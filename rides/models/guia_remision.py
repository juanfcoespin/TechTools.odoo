# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ..utils import convertion_utils


class GuiaRemision(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'rides.base']

    peso_total = fields.Float(
        string="Total Peso (kg)",
        compute="get_total_peso"
    )
    peso_total_qq = fields.Float(
        string="Total Peso (qq)",
        compute="get_total_peso_qq"
    )
    transportista_id = fields.Many2one("res.partner", string="Transportista")
    placa_vehiculo = fields.Char(
        string="Placa Vehículo",
        size=8
    )
    punto_partida = fields.Char("Punto de Partida")

    @api.constrains('name')
    def check_tipo_documento(self):
        self.set_default_tipo_documento()

    # peso en quintales
    def get_total_peso_qq(self):
        # por alguna extraña razon no se puede sobreescribir defaul_get()
        self.set_default_tipo_documento()
        self.peso_total_qq = convertion_utils.kg_to_quintales(self.peso_total)


    def set_default_tipo_documento(self):
        self.tipo_documento_id = self.get_first_tipo_documento(self, 'gu')

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
