# -*- coding: utf-8 -*-
from . import convertion_utils
from odoo import api, fields, models
from datetime import datetime


class Factura(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'rides.base']

    num_factura = fields.Char(
        string="No.",
        compute="get_num_factura"
    )
    clave_acceso = fields.Char(
        string="Clave de Acceso",
        compute="get_clave_acceso_factura"
    )
    
    ambiente = fields.Char(
        string="Ambiente",
        compute="get_ambiente_factura"
    )
    tipo_emision = fields.Char(
        string="Ambiente",
        compute="get_tipo_emision_factura"
    )
    fecha_autorizacion = fields.Datetime(
        string="Fecha y Hora Autorización",
        default=datetime.now()
    )

    def get_tipo_emision_factura(self):
        self.tipo_emision= self.get_tipo_emision()

    def get_ambiente_factura(self):
        self.ambiente= self.get_ambiente()

    def get_clave_acceso_factura(self):
        self.clave_acceso = self.get_clave_acceso('01', self.id, self.date)

    def get_num_factura(self):
        self.num_factura = self.get_num_ride(self.id)
