# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions, sql_db, SUPERUSER_ID
import logging


class TipoDocumento(models.Model):
    _name = 'res.tipo.documento'
    # se utiliza para asignar los puntos de emisión ej. FactElect 002, Nota crédito 003
    name = fields.Char(string="Tipo Documento", required=True)
    company_id = fields.Many2one("res.company")
    punto_emision = fields.Char(string="Punto Emisión Ej.: 001, 002", size=3, required=True)
    _sql_constraints = [
        ('punto_emision_uniq', 'unique (punto_emision)',
         "Ya existe un tipo de documento con este punto de emisión!!"),
        ('name_uniq', 'unique (name)',
         "Ya existe otro tipo de documento con este nombre!!"),
    ]

    @api.constrains('punto_emision')
    def check_tipo_documento(self):
        '''
                if not self.name:
            raise exceptions.UserError('Debe registrar el tipo de documento!!')
        if not self.punto_emision:
            raise exceptions.UserError('Debe registrar el código del punto de emisión!!')
        :return:
        '''

        try:
            int_value = int(self.punto_emision)
        except:
            raise exceptions.UserError('Punto de emision incorrecto!!')

