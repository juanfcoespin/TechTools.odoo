# pip3 install pyOpenSSL
from OpenSSL import crypto
# pip3 install signxml
from lxml import etree
from signxml import XMLSigner, XMLVerifier


class SignXML:
    def __init__(self, path_p12, pwd):
        self.path12 = path_p12
        self.pwd = pwd
        self.p12 = self.get_p12()

    def get_p12(self):
        with open(self.path12, 'rb') as file:
            return crypto.load_pkcs12(file.read(), self.pwd)

    def get_pem_private_key(self):
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, self.p12.get_privatekey())

    def get_pem_certificate(self):
        return crypto.dump_certificate(crypto.FILETYPE_PEM, self.p12.get_certificate())

    def get_signed_value(self, str_xml):
        cert = self.get_pem_certificate()
        key = self.get_pem_private_key()
        root = etree.fromstring(str_xml)
        signed_root = XMLSigner().sign(root, key=key, cert=cert)
        ms = XMLVerifier().verify(signed_root).signed_xml
        return ms
