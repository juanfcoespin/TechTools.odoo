# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions, sql_db, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


class Impuesto(models.Model):
    _name = 'account.tax'
    _inherit = ['account.tax']
    codigo_impuesto = fields.Integer(string="Código Impuesto SRI", default=2)
    codigo_porcentaje_impuesto = fields.Integer(string="Código Porcentaje Impuesto SRI", default=2)

