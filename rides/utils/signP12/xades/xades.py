# -*- coding: utf-8 -*-

import base64
import os
import subprocess
from lxml import etree
import logging

class Xades(object):

    def sign(self, xml_document, file_pk12, password):
        """
        Metodo que aplica la firma digital al XML
        Ejecutando una libreria .jar de JAVA
        """
        jar_path = os.path.join('jar', 'SignXades.jar')
        absolute_jar_path = os.path.join(os.path.dirname(__file__), jar_path)
        firma_path = self.get_64bits_string_representation(file_pk12)
        clave_firma = self.get_64bits_string_representation(password)
        command = [
            'java',
            '-jar',
            absolute_jar_path,
            xml_document,
            firma_path,
            clave_firma
        ]
        try:
            p = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            res = p.communicate()
            return res[0]
        except Exception as e:
            error = str(e)
            raise ValueError(error)

    def get_64bits_string_representation(self, me):
        ms = str(base64.b64encode(me.encode('utf-8')))
        ms = ms.replace("b'", "")
        ms = ms.replace("'", "")
        return ms
