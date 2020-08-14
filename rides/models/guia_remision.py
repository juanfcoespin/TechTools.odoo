# -*- coding: utf-8 -*-
from . import convertion_utils
from odoo import api, fields, models


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
    num_guia = fields.Char(
        string="No.",
        compute="get_num_guia"
    )
    clave_acceso = fields.Char(
        string="Clave de Acceso",
        compute="get_clave_acceso_guia",
    )
    
    ambiente = fields.Char(
        string="Ambiente",
        compute="get_ambiente_guia",
    )
    tipo_emision = fields.Char(
        string="Ambiente",
        compute="get_tipo_emision_guia",
    )
    transportista_id = fields.Many2one("res.partner", string="Transportista")
    placa_vehiculo = fields.Char(
        string="Placa Vehículo",
        size=8
    )
    punto_partida = fields.Char("Punto de Partida"
                                )
    def get_tipo_emision_guia(self):
        self.tipo_emision= self.get_tipo_emision()

    def get_ambiente_guia(self):
        self.ambiente= self.get_ambiente()

    def get_clave_acceso_guia(self):
        self.clave_acceso = self.get_clave_acceso('06', self.id, self.date)

    def get_num_guia(self):
        self.num_guia = self.get_num_ride(self.id)

    # peso en quintales
    def get_total_peso_qq(self):
        self.peso_total_qq = convertion_utils.kg_to_quintales(self.peso_total)

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
