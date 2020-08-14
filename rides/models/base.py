from odoo import api, fields, models


class Ride(models.AbstractModel):
    _name = 'rides.base'
    _description = 'Compendio de funciones generales para los rides'

    # 1 para pruebas, 2 para produccion
    cod_ambiente = "1"

    # 1 Emisión Normal
    cod_tipo_emision = "1"

    def get_ambiente(self):
        if self.cod_ambiente == "1":
            return "PRUEBAS"
        if self.cod_ambiente == "2":
            return "PRODUCCION"
        return ""
    def get_tipo_emision(self):
        if self.cod_tipo_emision == "1":
            return "NORMAL"
        return ""

    def get_secuencial(self, id_documento):
        # 145 -> '000000145'
        secuencial = str(id_documento).rjust(9, '0')
        return secuencial

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
    def get_clave_acceso(self, cod_tipo_documento, id_documento, fecha_documento):
        current_date = "{}{}{}".format(str(fecha_documento.day).rjust(2, '0'),
                                       str(fecha_documento.month).rjust(2, '0'),
                                       fecha_documento.year)
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
        # clave = "010420200117904628540012001010000068498123456781"
        dv = self.get_digito_verificador(clave)
        clave = "{}{}".format(clave, str(dv))
        return clave

    def get_digito_verificador(self, clave):
        clave_invertida = clave[::-1]
        sumandos = []
        i = 2

        for n in clave_invertida:
            if i == 8:
                i = 2
            sumandos.append(int(n)*i)
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



