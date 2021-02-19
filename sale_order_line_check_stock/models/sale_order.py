# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
from ..utils import common
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_id', 'product_uom_qty')
    def check_stock(self):
        if common.hay_productos_sin_stock(self):
            raise ValidationError('Algún producto no tiene stock. No se guardó el pedido!!')
