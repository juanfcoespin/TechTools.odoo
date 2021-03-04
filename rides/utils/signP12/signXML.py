# pip3 install pyOpenSSL
from OpenSSL import crypto
# pip3 install signxml
from lxml import etree
from signxml import XMLSigner, XMLVerifier
from lxml import etree as lxml_ET
import os
from os import path
import xml.etree.ElementTree as ET
import base64



class SignXML:
    def __init__(self, cert, cert_name, pwd):
        self.cert = cert
        self.cert_name = cert_name
        self.pwd = pwd
        self.p12 = self.get_p12()

    def get_p12(self):
        if self.cert is None or self.cert_name is None:
            raise Exception('No se ha subido el cerfificado digital de firma electronica')
        local_path = os.path.dirname(__file__)
        cert_path = os.path.join(local_path, self.cert_name)
        if not path.exists(cert_path):
            self.copy_cert(cert_path)
        with open(cert_path, 'rb') as file:
            return crypto.load_pkcs12(file.read(), self.pwd)

    def copy_cert(self, cert_path):
        buffer = open(cert_path, "wb")
        byte_array = base64.b64decode(self.cert)
        buffer.write(byte_array)
        buffer.close()

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
        cert = self.get_pem_certificate()
        key = self.get_pem_private_key()
        ET.register_namespace("ds", "http://www.w3.org/2000/09/xmldsig#")
        xml2 = str_xml.encode('utf -8')
        root = etree.fromstring(xml2)
        signed_root = XMLSigner().sign(root, key=key, cert=cert)
        data_serialized = lxml_ET.tostring(signed_root)
        data_parsed = ET.fromstring(data_serialized)
        tree = ET.ElementTree(data_parsed)
        tree.write(output_filename)
