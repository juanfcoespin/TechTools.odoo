# -*- coding: utf-8 -*-

from odoo import models, fields, exceptions, api


class ResCompanyEc(models.Model):
    _inherit = 'res.company'

    # para establecer los puntos de emisión por tipo de documento. Ej. Factura Física 001, Fact Electroncia 002
    punto_emision_ids = fields.One2many(
        comodel_name="tt_company.punto.emision",
        inverse_name="company_id",
        string="Puntos de Emisión"
    )


class PuntoEmision(models.Model):
    _name = 'tt_company.punto.emision'
    _description = 'Puntos de emisión para documentos electrónicos'
    # se utiliza para asignar los puntos de emisión ej. FactElect 002, Nota crédito 003
    name = fields.Char(string="Tipo Documento", required=True)
    cod_tipo_documento = fields.Char(string="Código Tipo Documento (SRI)", size=2, required=True)
    company_id = fields.Many2one("res.company")
    cod_punto_emision = fields.Char(string="Código Punto Emisión Ej.: 001, 002", size=3, required=True)
    ultimo_secuencial = fields.Integer(string="Último secuencial", default=1)
    _sql_constraints = [
        ('punto_emision_uniq', 'unique (punto_emision)',
         "Ya existe un tipo de documento con este punto de emisión!!"),
        ('name_uniq', 'unique (name)',
         "Ya existe otro tipo de documento con este nombre!!"),
    ]





