# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompanyEc(models.Model):
    _inherit = 'res.company'

    #info tributaria
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
    cod_establecimiento = fields.Char(string="Codigo Establecimiento",
                                      default="001", size=3)
    cod_punto_emision = fields.Char(string="Codigo Punto Emisión",
                                    default="002", size=3)
    ultimo_secuencial_factura = fields.Integer(string="Último secuencial factura", default=500)
    ultimo_secuencial_gr = fields.Integer(string="Último secuencial guía de Remisión", default=500)
    ultimo_secuencial_nc = fields.Integer(string="Último secuencial nota de crédito", default=500)
    # para establecer los puntos de emisión por tipo de documento. Ej. Factura Física 001, Fact Electroncia 002
    tipo_documento_ids = fields.One2many(
        comodel_name="res.tipo.documento",
        inverse_name="company_id",
        string="Documentos Electrónicos"
    )

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




