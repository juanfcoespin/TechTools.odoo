# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions, sql_db, SUPERUSER_ID
from datetime import datetime
from ..utils.xml.xml_doc import XmlDoc
from ..utils.signP12.signXML import SignXML
from ..utils import common
import os
from jinja2 import Environment, FileSystemLoader
from zeep import Client
import logging
import threading

_logger = logging.getLogger(__name__)


class Factura(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'rides.base']
    clave_acceso = fields.Char(string="Clave de Acceso", compute="init_ride")
    total_discount = fields.Float(
        string="Total Descuento",
        compute="get_total_discount"
    )
    iva = fields.Float(
        string="Iva",
        compute="get_iva"
    )
    total_con_impuestos = fields.Float(
        string="Total con impuestos",
        compute="get_total_con_impuestos"
    )
    total_sin_descuento = fields.Float(
        string="Total sin descuento",
        compute="get_total_sin_descuento"
    )


    @api.constrains('num_documento')
    def check_uniq_num_factura(self):
        fact_num = self.num_documento
        facturas_existentes=self.env['account.move'].\
            search([('num_documento', '=', self.num_documento), ('move_type', '=', 'out_invoice')])
        if len(facturas_existentes) > 1:
            raise exceptions.UserError('Ya existe la factura con el número ' + self.num_documento +
                                       '\n Por favor seleccione otro número')
    def init_ride(self):
        self.clave_acceso = self.init_ride_and_get_clave_acceso('01', self.date)

    def consultar_estado_autorizacion(self):
        if self.resp_sri is not None and self.enviado_al_sri:
            if self.company_id.factura_electronica_ambiente == '2':  # Produccion
                url = self.company_id.url_autorizacion_documentos
            else:
                url = self.company_id.url_autorizacion_documentos_prueba  # Pruebas
            client = Client(url)
            result = client.service.autorizacionComprobante(self.clave_acceso)
            if result and result.autorizaciones and result.autorizaciones.autorizacion and len(result.autorizaciones.autorizacion) > 0:
                estado = result.autorizaciones.autorizacion[0].estado
                self.autorizacion_sri = estado
            else:
                self.autorizacion_sri = result
        else:
            self.autorizacion_sri = "Primero debe enviarse el documento al SRI"

    def get_lines(self):
        detalles = []
        for line in self.invoice_line_ids:
            codigo_principal = line.product_id.id
            codigo_auxiliar = line.product_id.barcode
            priced = line.price_unit * (1 - (line.discount or 0.00) / 100.0)
            discount = (line.price_unit - priced) * line.quantity
            detalle = {
                'codigoPrincipal': codigo_principal,
                'codigoAuxiliar': codigo_auxiliar,
                'descripcion': line.name.strip(),
                'cantidad': '%.6f' % (line.quantity),
                'precioUnitario': '%.6f' % (line.price_unit),
                'descuento': '%.2f' % discount,
                'precioTotalSinImpuesto': '%.2f' % (line.price_subtotal)
            }
            impuestos = []
            for tax in line.tax_ids:
                if tax.description in ['IVA Cobrado 12%']:
                    impuesto = {
                        'codigo': 2,
                        'codigoPorcentaje': 2,  # noqa
                        'tarifa': tax.amount,
                        'baseImponible': '{:.2f}'.format(line.price_subtotal),
                        'valor': '{:.2f}'.format(line.price_subtotal *
                                                 tax.amount / 100)
                    }
                    impuestos.append(impuesto)
            detalle.update({'impuestos': impuestos})
            detalles.append(detalle)
        return detalles

    def safe_pdf_factura(self, pdf_path, pdf_filename):
        pdf_binary = common.get_pdf_report_binary(self, 'rides.factura')
        common.create_file_from_binary(pdf_binary,
                                       os.path.join(pdf_path, pdf_filename))

    def sign_and_safe_xml_factura(self, xml_path, xml_filename):
        doc = XmlDoc(self)
        # doc.render()
        str_xml = doc.get_xml_text_factura()
        cert = self.company_id.certificado_digital
        cert_name = self.company_id.document_name
        pwd = self.company_id.cert_pwd
        xml_signer = SignXML(cert, cert_name, pwd)
        xml_signer.sign_xml(str_xml,
                            os.path.join(xml_path, xml_filename))

    def _job_invoices_to_send_sri(self):
        '''
            check pull of invoices that need execute enviar_sri function
        :return:
        '''
        url = self.get_url_to_send_xml()
        _logger.debug(url)
        # ride_path = self.company_id.electronic_docs_path
        ride_path = '/Users/mac/Dropbox/TechTools/documentosEmpresa/comprobantesElectronicos'
        _logger.debug(ride_path)
        # dbname = threading.current_thread().dbname
        dbname = 'devTT'
        _logger.debug(dbname)
        ride_path = common.get_ride_path(ride_path, dbname)

        _logger.debug(ride_path)

        invoices = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('procesando_fec', '!=', True), # para evitar que se procese mas de una vez la misma factura
            ('move_type', '=', 'out_invoice'),
            '|', ('enviado_al_sri', '!=', True), ('email_enviado', '!=', True), ('pdf_generado', '!=', True)
        ])

        if invoices:
            for inv in invoices:
                self.enviar_sri(inv, url, ride_path)

    def enviar_sri(self, me=None, url=None, ride_path=None):
        '''
            - genera el pdf y el xml de la factura
            - envia por correo al cliente
            - envia al sri el xml firmado electrónicamente
        :return:
        '''
        try:
            if me is None:
                me = self

            me.procesando_fec = True
            self.env.cr.commit()
            if url is None:
                url = me.get_url_to_send_xml()
            if ride_path is None:
                ride_path = me.company_id.electronic_docs_path
                dbname = threading.current_thread().dbname
                ride_path = common.get_ride_path(ride_path, dbname)
            # to no call algorithm to generate clave_acceso more than one time
            _logger.debug(ride_path)
            clave_acceso = self.init_ride_and_get_clave_acceso('01', me.date)
            _logger.debug(clave_acceso)
            if not me.xml_generado:
                xml_path = common.get_ride_path(ride_path, 'xml')
                self.sign_and_safe_xml_factura(xml_path, clave_acceso + '.xml')
                self.xml_generado = True
            if not me.pdf_generado:
                pdf_path = common.get_ride_path(ride_path, 'pdf')
                self.safe_pdf_factura(pdf_path, clave_acceso + '.pdf')
                self.pdf_generado = True
            if not me.email_enviado:
                self.send_documents_by_mail()
            if not me.enviado_al_sri:
                self.send_xmlsigned_to_sri(url, ride_path, clave_acceso)
            me.procesando_fec = False
        except Exception as e:
            error = 'Error al enviar la factura al SRI:' + str(e)
            _logger.debug(error)
            exceptions.UserError(error)
            me.procesando_fec = False

    def send_xmlsigned_to_sri(self, url, ride_path, clave_acceso):
        try:
            client = Client(url)
            xml = self.get_signed_xml(os.path.join(ride_path, 'xml'),clave_acceso + '.xml')
            result = client.service.validarComprobante(xml)
            self.resp_sri = result
            self.enviado_al_sri = True
        except Exception as e:
            self.resp_sri = "El Servicio Web del Sri no está disponible en este momento. Error:"+str(e)
    def send_documents_by_mail(self):
        template_id = self.env.ref('rides.email_template_FEL').id
        template = self.env['mail.template'].browse(template_id)
        id_factura = self.id
        template.send_mail(id_factura, force_send=True)
        self.email_enviado = True

    def get_signed_xml(self, ride_path, xml_filename):
        env = Environment(loader=FileSystemLoader(ride_path))
        xml_fact = env.get_template(xml_filename)
        return xml_fact.render().encode('utf-8')

    def get_total_sin_descuento(self):
        self.total_sin_descuento = self.amount_untaxed + self.total_discount

    def get_total_con_impuestos(self):
        self.total_con_impuestos = round(self.amount_untaxed + self.iva, 2)

    def get_iva(self):
        self.iva = 0
        for group in self.amount_by_group:
            if group[0] == 'IVA 12%':
                self.iva = group[1]

    def get_total_discount(self):
        self.total_discount = 0
        for line in self.invoice_line_ids:
            line_subTotal = line.quantity * line.price_unit
            line_discount = line_subTotal * line.discount / 100
            self.total_discount += line_discount
        self.total_discount = round(self.total_discount, 2)
