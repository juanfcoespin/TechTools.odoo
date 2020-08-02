# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerEc(models.Model):
    _inherit = 'res.partner'

    ec_identifier_type = fields.Selection(
        string="Tipo Identificación",
        selection=[
            ('c', 'Cédula'),
            ('r', 'Ruc'),
            ('p', 'Pasaporte')
        ]
    )
    ec_identifier = fields.Char(string="Ruc / CI",
        help="Registro único de contribuyentes o cédula de identidad", size=13)


