# -*- coding: utf-8 -*-
from jinja2 import Template, Environment, FileSystemLoader
import logging
import os
from datetime import datetime
from ...utils import common


class XmlDoc:
    def __init__(self, ride):
        self.ride = ride
        self.loger = logging.getLogger(__name__)

    '''
        def render(self):
        ms = self.get_xml_text_factura()
        self.loger.info(ms)
        self.save_xml_ride(ms)
    '''

    def get_xml_text_factura(self):
        template = self.get_template()
        return self.render_ride(template)

    def render_ride(self, template):
        ride = self.ride
        comprador = ride.partner_id
        lines = ride.get_lines()
        factura_relacionada, motivo_nc = self.get_factura_relacionada()
        fecha_emision_doc_sustento = None
        if factura_relacionada:
            fecha_emision_doc_sustento=ride.get_ddmmyyy_date(factura_relacionada.date, '/')
        ms = template.render(
            ambiente=ride.cod_ambiente,
            tipoEmision=ride.cod_tipo_emision,
            razonSocial=common.clear_tildes(ride.company_id.razon_social),
            nombreComercial=common.clear_tildes(ride.company_id.name),
            ruc=ride.company_id.ruc,
            claveAcceso=ride.clave_acceso,
            codDocumento=ride.tipo_documento_id.cod_tipo_documento,
            estab=ride.company_id.cod_establecimiento,
            ptoEmi=ride.tipo_documento_id.cod_punto_emision,
            secuencial=ride.secuencial,
            dirMatriz=common.clear_tildes(ride.get_direccion()),
            fechaEmision=ride.get_ddmmyyy_date(ride.date, '/'),
            dirEstablecimiento=common.clear_tildes(ride.get_direccion()),
            contribuyenteEspecial=ride.company_id.nro_contribuyente_especial,
            obligadoContabilidad=ride.company_id.obligado_llevar_contabilidad,
            rise=ride.company_id.rise,
            tipoIdentificacionComprador=comprador.ec_identifier_type,
            razonSocialComprador=common.clear_tildes(comprador.name),
            identificacionComprador=comprador.ec_identifier,
            direccionComprador=common.clear_tildes(comprador.invoice_address),
            totalSinImpuestos=ride.amount_untaxed,
            totalDescuento=ride.total_discount,
            totalConImpuesto=ride.total_con_impuestos,
            lines=lines,
            impuestos=ride.get_total_impuestos(),
            facturaRelacionada=factura_relacionada,
            motivoNc=motivo_nc,
            fechaEmisionDocSustento=fecha_emision_doc_sustento,
        )
        return ms

    def get_factura_relacionada(self):
        ride = self.ride
        cod_tipo_documento = ride.tipo_documento_id.cod_tipo_documento
        if cod_tipo_documento == '04':  # si es nota de crédito
            fact_name, motivo = self.get_fact_name_from_ref(ride.ref)
            if fact_name:
                factura_relacionada = ride.env['account.move'].search([('name', '=', fact_name)])
                return factura_relacionada, motivo
        return None, None

    def get_fact_name_from_ref(self, ref):
        '''
            returns fact name from ref fielf of NC
        :param ref: Ex: Reversal of: INV/2021/06/0001, Devolución
        :return: fact name: INV/2021/06/0001
        '''
        if ref:
            matrix = ref.split(",")
            if len(matrix) == 2:
                fact_name = matrix[0]
                fact_name = fact_name.replace("Reversal of: ", "")
                motivo = matrix[1]
                return fact_name, motivo

        return None, None


    def get_template(self):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(template_path))
        ride = self.ride
        cod_tipo_documento = ride.tipo_documento_id.cod_tipo_documento
        template_file_name = None
        if cod_tipo_documento == '01':
            template_file_name = 'factura.xml'
        if cod_tipo_documento == '04':
            template_file_name = 'notaCredito.xml'
        if not template_file_name:
            return None
        return env.get_template(template_file_name)
