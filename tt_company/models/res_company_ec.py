# -*- coding: utf-8 -*-

from odoo import models, fields, exceptions, api


class ResCompanyEc(models.Model):
    _inherit = 'res.company'
    # info tributaria
    ruc = fields.Char(string="Ruc",
                      help="Registro único de contribuyentes", size=13)
    razon_social = fields.Char(string="Razón Social")
    obligado_llevar_contabilidad = fields.Selection(
        [
            ('SI', 'SI'),
            ('NO', 'NO')
        ],
        string='Obligado a llevar contabilidad',
        default='NO'
    )
    nro_contribuyente_especial = fields.Integer(string="Nro. Contribuyente Especial")
    rise = fields.Boolean(
        string='Contribuyente Régimen Simplificado RISE',
        default=False
    )
    cod_establecimiento = fields.Char(string="Codigo Establecimiento",
                                      default="001", size=3)
    # facturación electrónica
    factura_electronica_ambiente = fields.Selection(
        [
            ('1', 'Pruebas'),
            ('2', 'Producción')
        ],
        string='Ambiente',
        default='1'
    )
    factura_electronica_tipo_emision = fields.Selection(
        [
            ('1', 'Normal'),
            ('2', 'Extraordinario')
        ],
        string='Tipo de emisión',
        default='1'
    )
    certificado_digital = fields.Binary(string="Certificado Digital ext p12")
    document_name = fields.Char(string="Nombre Certificado")
    cert_pwd = fields.Char(string="Contraseña Certificado")
    electronic_docs_path = fields.Char(string="Ruta Carpeta Comprobantes Elctrónicos")
    url_recepcion_documentos_prueba = \
        fields.Char(string="Url Recepcion Documentos Prueba",
                    default="https://celcer.sri.gob.ec/comprobantes-electronicos-ws"
                            "/RecepcionComprobantesOffline?wsdl")
    url_autorizacion_documentos_prueba = \
        fields.Char(string="Url Autorizacion Documentos Prueba",
                    default="https://celcer.sri.gob.ec/comprobantes-electronicos-ws"
                            "/AutorizacionComprobantesOffline?wsdl")
    url_recepcion_documentos = \
        fields.Char(string="Url Recepcion Documentos",
                    default="https://cel.sri.gob.ec/comprobantes-electronicos-ws"
                            "/RecepcionComprobantesOffline?wsdl")
    url_autorizacion_documentos = \
        fields.Char(string="Url Autorizacion Documentos",
                    default="https://cel.sri.gob.ec/comprobantes-electronicos-ws"
                            "/AutorizacionComprobantesOffline?wsdl")

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





