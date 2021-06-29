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

    def render(self):
        ms = self.get_xml_text_factura()
        self.loger.info(ms)
        self.save_xml_ride(ms)

    def get_xml_text_factura(self):
        template = self.get_template()
        return self.render_factura(template)

    def render_factura(self, template):
        ride = self.ride
        comprador = ride.partner_id
        lines = ride.get_lines()
        for item in lines:
            item['descripcion'] = common.clear_tildes(item['descripcion'])

        ms = template.render(
            ambiente=ride.cod_ambiente,
            tipoEmision=ride.cod_tipo_emision,
            razonSocial=common.clear_tildes(ride.company_id.razon_social),
            nombreComercial=common.clear_tildes(ride.company_id.name),
            ruc=ride.company_id.ruc,
            claveAcceso=ride.clave_acceso,
            estab=ride.company_id.cod_establecimiento,
            ptoEmi=ride.tipo_documento_id.cod_punto_emision,
            secuencial=ride.secuencial,
            dirMatriz=common.clear_tildes(ride.get_direccion()),
            fechaEmision=ride.get_ddmmyyy_date(ride.date, '/'),
            dirEstablecimiento=common.clear_tildes(ride.get_direccion()),
            contribuyenteEspecial=ride.company_id.nro_contribuyente_especial,
            obligadoContabilidad=ride.company_id.obligado_llevar_contabilidad,
            tipoIdentificacionComprador=comprador.ec_identifier_type,
            razonSocialComprador=common.clear_tildes(comprador.name),
            identificacionComprador=comprador.ec_identifier,
            direccionComprador=common.clear_tildes(comprador.invoice_address),
            totalSinImpuestos=ride.amount_untaxed,
            totalDescuento=ride.total_discount,
            totalConImpuesto=ride.total_con_impuestos,
            lines=lines,
            impuestos=ride.get_total_impuestos()
        )
        return ms

    def get_template(self):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(template_path))
        template_file_name = 'factura.xml'
        if self.ride.company_id.nro_contribuyente_especial > 0:
            template_file_name = 'facturaContribuyenteEspecial.xml'
        return env.get_template(template_file_name)
