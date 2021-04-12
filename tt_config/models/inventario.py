# -*- coding: utf-8 -*-
from odoo import models, exceptions, fields
import logging

_logger = logging.getLogger(__name__)


class InventarioConfig2(models.Model):
    _name = 'tt_config.inventario'
    _description = 'Configuraciones adicionales de inventario'
    cost_type = fields.Selection(
        string="Tipo de costo",
        selection=[
            ('nd', 'No Definido'),
            ('avg', 'Promedio de precios de compra'),
            ('last', 'Último precio de compra'),
        ],
        default='nd',
        change_default=True,
        default_model='product.template'
    )

    def update_product_cost(self):
        try:
            if self.cost_type and self.cost_type != 'nd':
                products_without_cost = self.env["product.template"].search([("standard_price", "=", 0)])
                for product in products_without_cost:
                    if self.cost_type == 'avg':
                        cost = self.get_avg_purchase_price_by_product(product.id)
                    if self.cost_type == 'last':
                        cost = self.get_last_purchase_price_by_product(product.id)
                    if cost > 0:
                        product.standard_price = cost
            else:
                raise exceptions.UserError('Debe seleccionar el método de costeo')
        except Exception as e:
            msg = str(e)
            raise exceptions.UserError('Error:\n'+msg)

    def get_last_purchase_price_by_product(self, id_product):
        # por defecto trae la orden mas reciente
        order_lines = self.env["purchase.order.line"].search([("product_id.id", "=", id_product)], limit=1)
        if order_lines and order_lines.id: #si hay una ordern de compra
            return order_lines.price_unit
        return 0

    def get_avg_purchase_price_by_product(self, id_product):
        order_lines = self.env["purchase.order.line"].search([("product_id.id", "=", id_product)])
        if order_lines and len(order_lines) > 0: #si hay ordenes de compra
            sum_prices = 0
            num_orders = 0
            for order in order_lines:
                sum_prices += order.price_unit
                num_orders += 1
            if num_orders > 0:
                avg_cost = sum_prices / num_orders
                return avg_cost
        return 0
