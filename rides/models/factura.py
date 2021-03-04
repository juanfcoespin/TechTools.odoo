# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
from ..utils.xml.xml_doc import XmlDoc
from ..utils.signP12.signXML import SignXML
import os
from jinja2 import Template, Environment, FileSystemLoader
from zeep import Client

import logging

_logger = logging.getLogger(__name__)


class Factura(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'rides.base']

    num_factura = fields.Char(
        string="No.",
        compute="get_num_factura"
    )
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
    total_mas_iva = fields.Float(
        string="Total mas Iva",
        compute="get_total_mas_iva"
    )
    total_sin_descuento = fields.Float(
        string="Total sin descuento",
        compute="get_total_sin_descuento"
    )

    def enviar_sri(self):
        url = None
        if self.company_id.factura_electronica_ambiente == 2:  # Produccion
            url = self.company_id.url_recepcion_documentos
        else:
            url = self.company_id.url_recepcion_documentos_prueba  # Pruebas
        if url is not None:
            xml = self.get_signed_xml()
            client = Client(url)
            result = client.service.validarComprobante(xml)
        tmp2 = 'hola'

    def get_signed_xml_mock(self):
        template_path = os.path.dirname(__file__)
        env = Environment(loader=FileSystemLoader(template_path))
        xml_fact = env.get_template('example.xml')
        return xml_fact.render().encode('utf-8')

    def get_signed_xml(self):
        ride_path = self.company_id.xml_path
        if ride_path is None:
            raise Exception('Debe configurar la ruta de destino de los rides')
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

    def get_total_mas_iva(self):
        self.total_mas_iva = self.amount_untaxed + self.iva

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


