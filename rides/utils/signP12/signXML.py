# pip3 install pyOpenSSL
from OpenSSL import crypto
# pip3 install signxml
from lxml import etree
from signxml import XMLSigner, XMLVerifier
from lxml import etree as lxml_ET

import os
import xml.etree.ElementTree as ET


class SignXML:
    def __init__(self, cert, pwd):
        self.cert = cert
        self.pwd = pwd
        self.p12 = self.get_p12()

    def get_p12(self):
        if self.cert is not None:
            return crypto.load_pkcs12(self.cert, self.pwd)
        return None

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

    def get_signed_value(self, str_xml):
        cert = self.get_pem_certificate()
        key = self.get_pem_private_key()
        ET.register_namespace("ds", "http://www.w3.org/2000/09/xmldsig#")

        xml2 = str_xml.encode('utf -8')
        root = etree.fromstring(xml2)
        signed_root = XMLSigner().sign(root, key=key, cert=cert)
        data_serialized = lxml_ET.tostring(signed_root)
        data_parsed = ET.fromstring(data_serialized)

        tree = ET.ElementTree(data_parsed)
        # tree.write("/Users/mac/Dropbox/new_signed_file4.xml")
        tree.write("c:\\tmp\\new_signed_file4.xml")
        # ms = XMLVerifier().verify(signed_root).signed_xml
