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
        template_path = os.path.dirname(__file__)
        env = Environment(loader=FileSystemLoader(template_path))
        xml_fact = env.get_template('example.xml')
        tmp = xml_fact.render()
        url = 'https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl '
        client = Client(url)
        result = client.validarComprobante(tmp)
        tmp2 = 'hola'

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



    def enviar_sri2(self):
        doc = XmlDoc(self)
        doc.render()
        str_xml = doc.get_xml_text_factura()
        url_p12 = 'c:\\tmp\\KARLA ELIZABETH PONCE FLORES 300720195029.p12'
        # url_p12 = '/Users/mac/Dropbox/TechTools/Proyectos/SistemaFacturacion/facturaElectronica/firmaElectronica/certificado/KARLA ELIZABETH PONCE FLORES 300720195029.p12'
        pwd = 'S1st3m4sJBP'