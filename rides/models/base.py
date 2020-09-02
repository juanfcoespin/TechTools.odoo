import logging
from odoo import api, fields, models


class Ride(models.AbstractModel):
    _name = 'rides.base'
    _description = 'Compendio de funciones generales para los rides'

    cod_ambiente = fields.Char(compute="set_ambiente")
    ambiente = fields.Char(compute="set_ambiente")

    cod_tipo_emision = fields.Char(compute="set_tipo_emision")
    tipo_emision = fields.Char(compute="set_tipo_emision")


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

    def get_secuencial(self, id_documento):
        # 145 -> '000000145'
        secuencial = str(id_documento).rjust(9, '0')
        return secuencial

    def get_direccion(self):
        return "{} y {}".format(self.company_id.street, self.company_id.street2)

    def get_num_ride(self, id_documento):
        return "{}-{}-{}".format(
            self.company_id.cod_establecimiento,
            self.company_id.cod_punto_emision,
            self.get_secuencial(id_documento)
        )

    '''
        Código Tipo Documento:
        01 Factura
        03 Liquidación de compra de bienes y prestación de servicios
        04 Nota de Crédito
        05 Nota de Débito
        06 Guía de Remisión
        07 Comprobante de Retención
    '''

    def get_clave_acceso(self, cod_tipo_documento, id_documento,  fecha_documento):
        current_date = self.get_ddmmyyy_date(fecha_documento)
        num_emisor = "12345678"
        clave = "{}{}{}{}{}{}{}{}{}".format(
            current_date,
            cod_tipo_documento,
            self.company_id.ruc,
            self.cod_ambiente,
            self.company_id.cod_establecimiento,
            self.company_id.cod_punto_emision,
            self.get_secuencial(id_documento),
            num_emisor,
            self.cod_tipo_emision
        )
        # clave = "010420200117904628540012001010000068498123456781" (sin dv)
        dv = self.get_digito_verificador(clave)
        clave = "{}{}".format(clave, str(dv))
        return clave

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
