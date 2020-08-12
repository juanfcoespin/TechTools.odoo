# -*- coding: utf-8 -*-

from odoo import api, fields, models
from . import utils


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    peso_total = fields.Float(
        string="Total Peso (kg)",
        compute="get_total_peso"
    )
    peso_total_qq = fields.Float(
        string="Total Peso (qq)",
        compute="get_total_peso_qq"
    )
    num_guia = fields.Char(
        string="No.",
        compute="get_num_guia"
    )
    clave_acceso = fields.Char(
        string="No.",
        compute="get_clave_acceso_guia"
    )

    def get_clave_acceso_guia(self):
        self.clave_acceso = utils.get_clave_acceso()

    def get_num_guia(self):
        company = self.env.user.company_id
        self.num_guia = utils.get_num_ride(company, self.id)

    # peso en quintales
    def get_total_peso_qq(self):
        self.peso_total_qq = utils.kg_to_quintales(self.peso_total)

    def get_total_peso(self):
        self.peso_total = 0
        for line in self.move_ids_without_package:
            peso_producto = line.product_id.weight
            peso_linea = peso_producto * line.product_uom_qty
            self.peso_total += peso_linea


class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    peso_producto = fields.Float(
        string="Peso Unit. (Kg)",
        compute="get_peso_producto"
    )
    peso_linea = fields.Float(
        string="Subtotal Peso",
        compute="get_peso_linea"
    )

    @api.onchange('product_id')
    def get_peso_producto(self):
        for line in self:
            line.peso_producto = line.product_id.weight

    @api.onchange('product_id', 'product_uom_qty')
    def get_peso_linea(self):
        for line in self:
            line.peso_linea = line.product_uom_qty * line.peso_producto
