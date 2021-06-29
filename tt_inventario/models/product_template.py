# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    '''
    @api.constrains('name')
    def validate_product(self):
        if not self.barcode:
            raise exceptions.UserError('Debe registrar el código de barras del producto!!')

    '''


