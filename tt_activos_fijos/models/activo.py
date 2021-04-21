# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Activo(models.Model):
    _name = 'tt_activos_fijos.activo'
    _description = 'Gestion de Activos'

    name = fields.Char("Name")
    product_id = fields.Many2one('product.product', string='Producto')
    modelo = fields.Char("Modelo")
    nro_serie = fields.Char(string="Nro. Serie")
    fecha_compra = fields.Date("Fecha de Compra", default=fields.Date.today)
    caracteristicas = fields.Many2many(comodel_name="tt_activos_fijos.caracteristica")
    asignacion_activo_line_ids = fields.One2many(
        comodel_name="tt_activos_fijos.asignacion_activo",
        inverse_name="activo_id",
        string="Asignacion Activo"
    )

    _sql_constraints = [
        ('nro_serie_uniq', 'unique (nro_serie)',
         "Nro. Serie Duplicado")
    ]

    @api.model
    def create(self, vals):
        '''
        inserta la secuencia en el campo name de la tabla
        Se pone "New" si no encuentra la secuencia
        '''
        seq_name = self.env['ir.sequence'].next_by_code(
            'seq_activo') or 'Nuevo'
        vals.update(name=seq_name)

        # la funcion create hace un insert en la tabla
        res = super(Activo, self).create(vals)
        return res


class CaracteristicaActivo(models.Model):
    _name = "tt_activos_fijos.caracteristica"
    name = fields.Char("Caracteristica")

class AsignacionActivo(models.Model):
    _name = 'tt_activos_fijos.asignacion_activo'
    _description = 'Asignacion de activo'

    custodio_actual = fields.Boolean(string="Custodio Actual", default=False)
    activo_id = fields.Many2one("tt_activos_fijos.activo")
    custodio_id = fields.Many2one("res.partner", string="Custodio")
    fecha_asignacion = fields.Date("Fecha Asignación", default=fields.Date.today)
    observaciones = fields.Char("Observaciones")

    @api.constrains('custodio_actual')
    def _check_unique_custodio(self):
        #    Valida que solo exista un custodio activo
        if self.custodio_actual:
            custodios_activos = self.search([('custodio_actual', '=', True),
                                             ('activo_id', '=', self.activo_id.id)])
            if custodios_activos and len(custodios_activos) > 1:
                raise exceptions.ValidationError("Sólo puede haber un custodio activo")

    @api.constrains('fecha_asignacion')
    def _check_unique_fecha_asignacion(self):
        #    Valida que no se dupliquen fechas de asignación
        if self.fecha_asignacion:
            records = self.search([('fecha_asignacion', '=', self.fecha_asignacion),
                                             ('activo_id', '=', self.activo_id.id)])
            if records and len(records) > 1:
                raise exceptions.ValidationError("Fecha de asignación duplicada")


