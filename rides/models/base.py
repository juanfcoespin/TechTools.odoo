import logging
from odoo import api, fields, models
from datetime import datetime


class Ride2(models.AbstractModel):
    '''def __init__(self, pool, cr, ride_type):
        self.ride_type = ride_type'''

    _name = 'rides.base'
    _description = 'Compendio de funciones generales para los rides'
    cod_ambiente = fields.Char(compute="set_ambiente")
    ambiente = fields.Char(compute="set_ambiente")
    fecha_autorizacion = fields.Datetime(
        string="Fecha y Hora Autorización",
        default=datetime.now()
    )
    cod_tipo_emision = fields.Char(compute="set_tipo_emision")
    tipo_emision = fields.Char(compute="set_tipo_emision")
    secuencial = fields.Char(string="secuencial")
    num_documento = fields.Char(string="Num Documento")
    enviado_al_sri = fields.Boolean(string="Enviado al SRI")
    pdf_generado = fields.Boolean(string="Pdf Generado")
    email_enviado = fields.Boolean(string="Email enviado al cliente")
    resp_sri = fields.Char(string="Respuesta SRI")
    autorizacion_sri = fields.Char(string="Estado autorización SRI")

    def init_ride_and_get_clave_acceso(self, cod_tipo_documento, ride_date):
        '''
         establece el secuencial, numero de documento y clave de acceso
        :param cod_tipo_documento:
            01 Factura
            03 Liquidación de compra de bienes y prestación de servicios
            04 Nota de Crédito
            05 Nota de Débito
            06 Guía de Remisión
            07 Comprobante de Retención
        :return:
        '''
        if not self.secuencial:
            ultimo_secuencial=self.get_ultimo_secuencia(cod_tipo_documento)
            self.secuencial = str(ultimo_secuencial).rjust(9, '0')
        if not self.num_documento:
            self.num_documento = self.get_num_ride(self.secuencial)
        return self.get_clave_acceso(cod_tipo_documento, ride_date)

    def get_ultimo_secuencia(self, ride_type):
        if ride_type == '01':
            ultimo_secuencial = self.company_id.ultimo_secuencial_factura + 1
            self.company_id.ultimo_secuencial_factura = ultimo_secuencial
        if ride_type == '06':
            ultimo_secuencial = self.company_id.ultimo_secuencial_gr + 1
            self.company_id.ultimo_secuencial_gr = ultimo_secuencial
        return ultimo_secuencial

    def get_clave_acceso(self, cod_tipo_documento, ride_date):
        '''

        :param cod_tipo_documento:
                01 Factura
                03 Liquidación de compra de bienes y prestación de servicios
                04 Nota de Crédito
                05 Nota de Débito
                06 Guía de Remisión
                07 Comprobante de Retención
        :param ride_date:
        :return:
        '''
        current_date = self.get_ddmmyyy_date(ride_date)
        num_emisor = "12345678"  # es el valor por defecto que pide el SRI
        clave = "{}{}{}{}{}{}{}{}{}".format(
            current_date,
            cod_tipo_documento,
            self.company_id.ruc,
            self.cod_ambiente,
            self.company_id.cod_establecimiento,
            self.company_id.cod_punto_emision,
            self.secuencial,
            num_emisor,
            self.cod_tipo_emision
        )
        # clave = "010420200117904628540012001010000068498123456781" (sin dv)
        dv = self.get_digito_verificador(clave)
        clave = "{}{}".format(clave, str(dv))
        return clave

    def set_ambiente(self):
        self.cod_ambiente = self.company_id.factura_electronica_ambiente
        self.ambiente = self.get_selection_name('res.company',
                                                'factura_electronica_ambiente',
                                                self.cod_ambiente)

    def set_tipo_emision(self):
        self.cod_tipo_emision = self.company_id.factura_electronica_tipo_emision
        self.tipo_emision = self.get_selection_name('res.company',
                                                    'factura_electronica_tipo_emision',
                                                    self.cod_tipo_emision)

    def get_selection_name(self, model, field, value):
        return dict(
            self.env[model].fields_get(field,
                                       'selection').get(field, {}).get('selection',
                                                                       {})).get(value)

    def get_direccion(self):
        return "{} y {}".format(self.company_id.street, self.company_id.street2)

    def get_num_ride(self, secuencial):
        return "{}-{}-{}".format(
            self.company_id.cod_establecimiento,
            self.company_id.cod_punto_emision,
            secuencial
        )





    def get_ddmmyyy_date(self, fecha, token=''):
        return "{}{}{}{}{}".format(str(fecha.day).rjust(2, '0'),
                                   token,
                                   str(fecha.month).rjust(2, '0'),
                                   token,
                                   fecha.year)

    def get_digito_verificador(self, clave):
        clave_invertida = clave[::-1]
        sumandos = []
        i = 2

        for n in clave_invertida:
            if i == 8:
                i = 2
            sumandos.append(int(n) * i)
            i += 1

        total = 0
        for sumando in sumandos:
            total += sumando
        op_modulo = total % 11
        digito_verificador = 11 - op_modulo
        if digito_verificador == 11:
            digito_verificador = 0
        if digito_verificador == 10:
            digito_verificador = 1
        return digito_verificador

    def get_fecha_hora(self, document_date):
        ms = "{}/{}/{} {}:{}:{}.000".format(
            str(document_date.day).rjust(2, '0'),
            str(document_date.month).rjust(2, '0'),
            document_date.year,
            str(document_date.hour).rjust(2, '0'),
            str(document_date.minute).rjust(2, '0'),
            str(document_date.second).rjust(2, '0'),
        )
        return ms

    def get_url_to_send_xml(self):
        if self.company_id.factura_electronica_ambiente == '2':  # Produccion
            ms = self.company_id.url_recepcion_documentos
        else:
            ms = self.company_id.url_recepcion_documentos_prueba  # Pruebas
        if ms is None:
            raise Exception('Debe registrar las Urls de comunicación con el SRI')
        return ms
