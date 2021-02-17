# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
from ..utils.xml.xml_doc import XmlDoc
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
    retencion_iva = fields.Float(
        string="% Retención Iva",
        compute="get_retencion_iva"
    )
    retencion_renta = fields.Float(
        string="% Retención Renta",
        compute="get_retencion_renta"
    )
    amount_total = fields.Float(
        string="Total menos retenciones",
        compute="get_total_menos_retenciones"
    )


    def get_total_menos_retenciones(self):
        self.amount_total = \
            self.amount_untaxed + self.amount_tax - self.retencion_iva - \
            self.retencion_renta

    # calcula el % de retencion del iva por cliente
    def get_retencion_iva(self):
        self.retencion_iva = 0
        # se evalua si en la factura aplica el iva
        if self.partner_id.ec_porcentaje_retencion_iva > 0 and\
                len(self.amount_by_group) > 0 and\
                self.amount_by_group[0][0] == 'IVA 12%':
            # el valor del iva por el % de retencion del socio de negocio
            self.retencion_iva = self.partner_id.ec_porcentaje_retencion_iva *\
                                 self.amount_by_group[0][1] / 100

    # calcula el % de retencion a la renta del socio de negocio
    def get_retencion_renta(self):
        self.retencion_renta = 0
        # se evalua si en la factura aplica el iva
        if self.partner_id.ec_porcentaje_retencion_renta > 0:
            # el valor de la base imponible por el % de retencion del socio de negocio
            self.retencion_renta = self.partner_id.ec_porcentaje_retencion_renta * \
                                 self.amount_untaxed / 100
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
        self.enviar_sri()
        return ms

    def get_secuencial_factura(self):
        self.secuencial = self.get_secuencial(self.id)

    def get_clave_acceso_factura(self):
        self.clave_acceso = self.get_clave_acceso('01', self.id, self.date)

    def enviar_sri(self):
        doc = XmlDoc(self)
        doc.render()


    def get_num_factura(self):
        self.num_factura = self.get_num_ride(self.id)
