# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Activo(models.Model):
    _name = 'tt_activos_fijos.activo'
    _description = 'Gestion de Activos'

    name = fields.Char("Código de Activo")
    product_id = fields.Many2one('product.product', string='Producto')
    custodio_id = fields.Many2one("hr.employee", string="Custodio")
    fecha_asignacion = fields.Date("Fecha Asignación", default=fields.Date.today)
    estado = fields.Selection(
        string="Estado",
        selection=[
            ('a', 'Activo'),
            ('o', 'Obsoleto'),
            ('b', 'Dado de Baja'),
        ]
    )
    foto = fields.Binary(readonly=False)

    '''
    Hay que mapear el pedido porque el mismo producto puede ser comprado varias veces
    Pero es un solo activo caracterizado por su código y número de serie
    '''
    pedido_compra = fields.Many2one('purchase.order', string='Orden de Compra')
    modelo = fields.Char("Marca / Modelo")
    nro_serie = fields.Char(string="Nro. Serie")
    fecha_compra = fields.Date("Fecha de Compra", compute="get_fecha_compra")
    tiempo_vida_util = fields.Integer("Tiempo de Vida Útil en años")
    caracteristicas = fields.Many2many(comodel_name="tt_activos_fijos.caracteristica")
    ubicaciones = fields.Many2many(comodel_name="ubicacion")

    historico_asignaciones = fields.One2many(
        comodel_name="tt_activos_fijos.historico_asignaciones",
        inverse_name="activo_id",
        string="Historico Asignaciones"
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

    def get_fecha_compra(self):
        if self.pedido_compra:
            self.fecha_compra = self.pedido_compra.date_planned
        else:
            self.fecha_compra = None


class CaracteristicaActivo(models.Model):
    _name = "tt_activos_fijos.caracteristica"
    name = fields.Char("Caracteristica")


class HistoricoAsignaciones(models.Model):
    _name = 'tt_activos_fijos.historico_asignaciones'
    _description = 'Asignacion de activo'

    activo_id = fields.Many2one("tt_activos_fijos.activo")
    custodio_id = fields.Many2one("hr.employee", string="Custodio")
    fecha_asignacion = fields.Date("Fecha Asignación")
    fecha_entrega = fields.Date("Fecha Entrega", default=fields.Date.today)
    observaciones = fields.Char("Observaciones")

    _sql_constraints = [
        ('fecha_asinacion_uniq', 'unique (fecha_asignacion)',
         "Fecha de asignación duplicada")
    ]
    @api.constrains('custodio_actual')
    def _check_unique_custodio(self):
        #    Valida que solo exista un custodio activo
        if self.custodio_actual:
            custodios_activos = self.search([('custodio_actual', '=', True),
                                             ('activo_id', '=', self.activo_id.id)])
            if custodios_activos and len(custodios_activos) > 1:
                raise exceptions.ValidationError("Sólo puede haber un custodio activo")
