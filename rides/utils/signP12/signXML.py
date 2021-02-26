# pip3 install pyOpenSSL
from OpenSSL import crypto
# pip3 install signxml
from lxml import etree
from signxml import XMLSigner, XMLVerifier
import os
from jinja2 import Template, Environment, FileSystemLoader


class SignXML:
    def __init__(self, path_p12, pwd):
        self.path12 = path_p12
        self.pwd = pwd
        self.p12 = self.get_p12()

    def get_p12(self):
        with open(self.path12, 'rb') as file:
            return crypto.load_pkcs12(file.read(), self.pwd)

    def get_pem_private_key(self):
        key_binary = crypto.dump_privatekey(crypto.FILETYPE_PEM, self.p12.get_privatekey())
        return bytes.decode(key_binary, 'utf-8')

    def get_pem_certificate(self):
        cert_binary = crypto.dump_certificate(crypto.FILETYPE_PEM, self.p12.get_certificate())
        return bytes.decode(cert_binary, 'utf-8')

    def get_signed_value2(self, str_xml):
        data_to_sign = "<Test/>"
        pem_path = os.path.join(os.path.dirname(__file__), 'testCertificate\\example.pem')
        key_path = os.path.join(os.path.dirname(__file__), 'testCertificate\\example.key')
        cert = open(pem_path).read()
        key = open(key_path).read()
        root = etree.fromstring(data_to_sign)
        signed_root = XMLSigner().sign(root, key=key, cert=cert)
        verified_data = XMLVerifier().verify(signed_root).signed_xml
        return verified_data

    def get_signed_value(self, str_xml):
        cert = self.get_pem_certificate()
        key = self.get_pem_private_key()
        # root = etree.fromstring(str_xml)
        root = etree.fromstring('<test/>')
        signed_root = XMLSigner().sign(root, key=key, cert=cert)
        ms = XMLVerifier().verify(signed_root).signed_xml
        return ms
