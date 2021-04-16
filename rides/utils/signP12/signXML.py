# pip3 install pyOpenSSL
import base64
import os
import xml.etree.ElementTree as ET
from os import path

from OpenSSL import crypto
# pip3 install signxml
from lxml import etree
from lxml import etree as lxml_ET
from signxml import XMLSigner, XMLVerifier, methods
from .. import common
import base64
from .xades.xades import Xades
import logging

_logger = logging.getLogger(__name__)


class SignXML:
    def __init__(self, cert, cert_name, pwd):
        self.cert = cert
        self.cert_name = cert_name
        self.pwd = pwd
        self.p12 = self.get_p12()

    def get_p12(self):
        cert_path = self.get_p12_path()
        with open(cert_path, 'rb') as file:
            return crypto.load_pkcs12(file.read(), self.pwd)

    def get_p12_path(self):
        if self.cert is None or self.cert_name is None:
            raise Exception('No se ha subido el cerfificado digital de firma electronica')
        local_path = os.path.dirname(__file__)
        cert_path = os.path.join(local_path, self.cert_name)
        if not path.exists(cert_path):
            common.create_file_from_binary(self.cert, True)
        return cert_path

    def get_p12_from_path(self, path_p12):
        with open(path_p12, 'rb') as file:
            return crypto.load_pkcs12(file.read(), self.pwd)

    def get_pem_private_key(self):
        if self.p12 is None:
            return None
        key_binary = crypto.dump_privatekey(crypto.FILETYPE_PEM, self.p12.get_privatekey())
        return bytes.decode(key_binary, 'utf-8')

    def get_pem_certificate(self):
        if self.p12 is None:
            return None
        cert_binary = crypto.dump_certificate(crypto.FILETYPE_PEM, self.p12.get_certificate())
        return bytes.decode(cert_binary, 'utf-8')

    # return xml file path signed
    def sign_xml(self, str_xml, output_filename):
        xades = Xades()
        file_pk12 = self.get_p12_path()
        signed_document = xades.sign(str_xml, file_pk12, self.pwd)
        str_signed_xml = signed_document.decode('utf-8')
        with open(output_filename, "w") as text_file:
            text_file.write(str_signed_xml)

    def sign_xmlbk(self, str_xml, output_filename):
        cert = self.get_pem_certificate()
        key = self.get_pem_private_key()
        ET.register_namespace("ds", "http://www.w3.org/2000/09/xmldsig#")
        xml2 = str_xml.encode('utf -8')
        root = etree.fromstring(xml2)
        # signed_root = XMLSigner().sign(root, key=key, cert=cert)
        try:
            signed_root = XMLSigner(method=methods.enveloped, signature_algorithm='rsa-sha1', digest_algorithm="sha1").sign(root, key=key, cert=cert)
            signed_data = etree.tostring(signed_root)
            verified_data = XMLVerifier().verify(signed_data, x509_cert=cert)
        except Exception as e:
            msg = str(e)
        data_serialized = lxml_ET.tostring(signed_root)
        data_parsed = ET.fromstring(data_serialized)
        tree = ET.ElementTree(data_parsed)
        tree.write(output_filename)
