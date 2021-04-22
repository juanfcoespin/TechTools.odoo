# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Consumible(models.Model):
    _name = 'tt_activos_fijos.consumible'
    _description = 'Gestion de Consumibles'

    name = fields.Many2one('product.product', string='Consumible')
    stock = fields.Integer("Stock", compute="get_stock_from_product")
    asignacion_consumible_line_ids = fields.One2many(
        comodel_name="tt_activos_fijos.asignacion_consumible",
        inverse_name="consumible_id",
        string="Asignacion Consumible"
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "Consumible Duplicado!!")
    ]

    def get_stock_from_product(self):
        self.stock = self.name.qty_available


class AsignacionComsumible(models.Model):
    _name = 'tt_activos_fijos.asignacion_consumible'
    _description = 'Asignacion de consumible'

    consumible_id = fields.Many2one("tt_activos_fijos.consumible")
    custodio_id = fields.Many2one("hr.employee", string="Custodio")
    departamento_id = fields.Many2one("hr.department", string="Departamento")
    fecha_asignacion = fields.Date("Fecha Asignación", default=fields.Date.today)
    cantidad = fields.Integer("Cantidad")
    ubicaciones = fields.Many2many(comodel_name="ubicacion")

class Ubicacion(models.Model):
    _name = "ubicacion"
    name = fields.Char("Ubicación")

