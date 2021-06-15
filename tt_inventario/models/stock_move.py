# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = 'stock.move.line'
    num_factura = fields.Char(
        string="Número de Factura",
        compute="set_num_factura"
    )
    factura_id = fields.Many2one('account.move', 'Factura')

    def set_num_factura(self):
        for line in self:
            # si el movimiento corresponde a una salida de bodega
            num_factura = 'No Aplica'
            if line.reference.count('WH/OUT') > 0:
                num_orden = line.origin
                facturas = self.env['account.move'].search([('invoice_origin', '=', num_orden)])
                if facturas:
                    for factura in facturas:
                        num_factura = factura.num_documento
                        line.factura_id = factura
            line.num_factura = num_factura


