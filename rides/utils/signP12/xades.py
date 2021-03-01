import xmlsig
from xades.policy import GenericPolicyId
from xades import XAdESContext
from OpenSSL import crypto
from lxml import etree


class Xades:
    def __init__(self, path_p12, pwd):
        self.path_p12 = path_p12
        self.pwd = pwd

    def sign(self, str_xml):
        xml2 = str_xml.encode('utf -8')
        root = etree.fromstring(xml2)
        policy = GenericPolicyId(
            "http://www.facturae.es/politica_de_firma_formato_facturae/"
            "politica_de_firma_formato_facturae_v3_1.pdf",
            u"Politica de Firma FacturaE v3.1",
            xmlsig.constants.TransformSha1,
        )
        ctx = XAdESContext(policy)

        with open(self.path_p12, "rb") as key_file:
            ctx.load_pkcs12(crypto.load_pkcs12(key_file.read(), self.pwd))
        ctx.sign(root)
        tmp = ctx
