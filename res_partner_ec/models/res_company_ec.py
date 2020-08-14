# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompanyEc(models.Model):
    _inherit = 'res.company'

    ruc = fields.Char(string="Ruc",
        help="Registro único de contribuyentes", size=13)
    cod_establecimiento = fields.Char(string="Codigo Establecimiento",
                                      default="001", size=3)
    cod_punto_emision = fields.Char(string="Codigo Punto Emisión",
                                      default="002", size=3)
    obligado_llevar_contabilidad = fields.Selection(
        [
            ('SI', 'SI'),
            ('NO', 'NO')
        ],
        string='Obligado a llevar contabilidad',
        default='NO'
    )
    nro_contribuyente_especial = fields.Integer(string="Nro. Contribuyente Especial")


