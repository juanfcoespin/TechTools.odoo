# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerEc(models.Model):
    _inherit = 'res.partner'

    ec_identifier_type = fields.Selection(
        string="Tipo Identificación",
        selection=[
            ('04', 'RUC'),
            ('05', 'CEDULA'),
            ('06', 'PASAPORTE'),
            ('07', 'VENTA A CONSUMIDOR FINAL'),
            ('08', 'IDENTIFICACION DEL EXTERIOR'),
        ]
    )
    ec_identifier = fields.Char(string="Ruc / CI",
        help="Registro único de contribuyentes o cédula de identidad", size=13)
    invoice_address = fields.Char(compute="set_invoice_address")
    delivery_address = fields.Char(compute="set_delivery_address")

    def set_invoice_address(self):
        if self.type == 'invoice':
            self.invoice_address = self.get_address(self)
        else:
            self.invoice_address = self.get_address_by_type('invoice')

    def set_delivery_address(self):
        self.invoice_address = self.get_address_by_type('delivery')

    def get_address_by_type(self, address_type):
        for address in self.child_ids:
            if address.type == address_type:
                return self.get_address(address)

    def get_address(self, address):
        return "{} y {}".format(address.street, address.street2)