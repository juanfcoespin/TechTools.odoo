# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    peso_total = fields.Float(
        string="Total Peso (Kg.)",
        compute="get_total_peso"
    )

    def get_total_peso(self):
        self.peso_total = 0
        for line in self.order_line:
            peso_producto = line.product_id.weight
            peso_linea = peso_producto * line.product_uom_qty
            self.peso_total +=  peso_linea


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    peso_producto = fields.Float(
        string="Peso Unit. (Kg)",
        compute="get_peso_producto"
    )
    peso_linea = fields.Float(
        string="Subtotal Peso",
        compute="get_peso_linea"
    )


    def get_peso_producto(self):
        for line in self:
            line.peso_producto = line.product_id.weight

    def get_peso_linea(self):
        for line in self:
            line.peso_linea = line.product_uom_qty * line.peso_producto


