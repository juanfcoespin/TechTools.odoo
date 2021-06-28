# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


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

    @api.constrains('name', 'ec_identifier')
    def check_uniq_cliente(self):
        if not self.name:
            raise exceptions.UserError('Debe registrar el nombre del cliente')
        #ilike compara mayusculas minusculas y tildes
        if self.ec_identifier:
            clientes_existentes = self.env['res.partner']. \
                search(['|', ('name', 'ilike', self.name), ('ec_identifier', '=', self.ec_identifier)])
            if len(clientes_existentes) > 1:
                raise exceptions.UserError('Ya existe el cliente con nombre o ruc/cedula: ' + self.name + ' ' + self.ec_identifier)
        else:
            clientes_existentes = self.env['res.partner']. \
                search([('name', 'ilike', self.name)])
            if len(clientes_existentes) > 1:
                raise exceptions.UserError('Ya existe el cliente ' + self.name)

        # valida que se ingresen clientes con cédula o ruc o consumidor final
        if self.name.lower() != 'consumidor final' and not self.ec_identifier:
            raise exceptions.UserError('No se puede registrar un cliente sin ruc o cédula!!')


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
