# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
from ..utils.xml.xml_doc import XmlDoc
from ..utils.signP12.signXML import SignXML
from ..utils import common
import os
from jinja2 import Environment, FileSystemLoader
from zeep import Client
from os import path
import logging
import threading

_logger = logging.getLogger(__name__)


class Factura(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'rides.base']

    num_factura = fields.Char(compute="get_num_factura")
    fecha_autorizacion = fields.Datetime(
        string="Fecha y Hora Autorización",
        default=datetime.now()
    )

    secuencial = fields.Char(compute="get_secuencial_factura")
    clave_acceso = fields.Char(compute="get_clave_acceso_factura")
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
    resp_sri = fields.Char(string="Respuesta SRI")
    autorizacion_sri = fields.Char(string="Estado autorización SRI")

    def consultar_estado_autorizacion(self):
        if self.resp_sri is None:
            raise Exception('Primero debe enviar el documento al SRI!!')
            return
        if self.company_id.factura_electronica_ambiente == 2:  # Produccion
            url = self.company_id.url_autorizacion_documentos
        else:
            url = self.company_id.url_autorizacion_documentos_prueba  # Pruebas
        client = Client(url)
        result = client.service.autorizacionComprobante(self.clave_acceso)
        # estado = result.autorizaciones.autorizacion[0].estado
        self.autorizacion_sri = result

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
                                                 tax.amount/100)
                    }
                    impuestos.append(impuesto)
            detalle.update({'impuestos': impuestos})
            detalles.append(detalle)
        return detalles

    def get_num_factura(self):
        self.num_factura = self.get_num_ride(self.id)

    def enviar_sri(self):
        if self.company_id.factura_electronica_ambiente == 2:  # Produccion
            url = self.company_id.url_recepcion_documentos
        else:
            url = self.company_id.url_recepcion_documentos_prueba  # Pruebas
        if url is not None:
            xml = self.get_signed_xml()
            client = Client(url)
            result = client.service.validarComprobante(xml)
            self.resp_sri = result
            # threaded_calculation = threading.Thread(target=self.call_ws_sri, args=(url, xml))
            # threaded_calculation.start()

    def save_pdf_ride(self):
        ms = {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Failure',
            'params': {
                'title': 'Postage Cancellation Failed',
                'text': 'Shipment is outside the void period.',
                'sticky': True
            }
        }
        return ms



    def call_ws_sri(self, url, xml):
        client = Client(url)
        result = client.service.validarComprobante(xml)
        self.save_resp_sri(result)

    def get_signed_xml_mock(self):
        template_path = os.path.dirname(__file__)
        env = Environment(loader=FileSystemLoader(template_path))
        xml_fact = env.get_template('example.xml')
        return xml_fact.render().encode('utf-8')

    def get_signed_xml(self):
        ride_path = self.company_id.electronic_docs_path
        if ride_path is None:
            raise Exception('Debe configurar la ruta de destino de los rides')
        ride_path = os.path.join(ride_path, 'xml')
        if not path.exists(ride_path):
            try:
                os.mkdir(ride_path)
            except OSError:
                raise Exception('no se pudo crear el directorio: ' + ride_path)
        doc = XmlDoc(self)
        # doc.render()
        str_xml = doc.get_xml_text_factura()
        cert = self.company_id.certificado_digital
        cert_name = self.company_id.document_name
        pwd = self.company_id.cert_pwd

        xml_signer = SignXML(cert, cert_name, pwd)
        xml_filename = self.clave_acceso+'.xml'
        xml_signer.sign_xml(str_xml, os.path.join(ride_path, xml_filename))
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

    @api.model
    def create(self, vals):
        # la funcion create hace un insert en la tabla
        ms = super(Factura, self).create(vals)
        # self.enviar_sri()
        return ms

    def get_secuencial_factura(self):
        self.secuencial = self.get_secuencial(self.id)

    def get_clave_acceso_factura(self):
        self.clave_acceso = self.get_clave_acceso('01', self.id, self.date)


