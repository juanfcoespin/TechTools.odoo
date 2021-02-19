# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def check_stock(self):
        for line in self:
            #si la cantidad del producto es mayor que el stock
            if(line.product_id and line.product_uom_qty > line.product_id.qty_available):
                mess = {
                    'title': 'Falta Stock!',
                    'message': 'Stock del producto no disponible para la cantidad ingresada!!'
                }
                return {'warning': mess}


