# install chilkat from https://www.example-code.com/python/rsa_sign_base64_pfx.asp
import sys
import chilkat
import base64


class SignP12:
    def __init__(self, path_p12, pwd, little_endian=False, encoding_mode='base64', hash_algorithm='sha-256'):
        self.path12 = path_p12
        self.pwd = pwd
        self.rsa = chilkat.CkRsa()
        # self.rsa.put_Utf8(True)
        self.pfx = chilkat.CkPfx()
        self.last_error = ''
        self.private_key = None
        self.little_endian = little_endian
        self.encoding_mode = encoding_mode
        self.hash_algorithm = hash_algorithm

    def get_signed_data(self, str_data):
        if self.p12_certificate_loaded():
            return self.rsa.signStringENC(str_data, self.hash_algorithm)
        return None

    def p12_certificate_loaded(self):
        if not self.pfx.LoadPfxFile(self.path12, self.pwd):
            self.last_error = self.pfx.lastErrorText()
        return self.load_private_key() and self.load_rsa()

    def load_private_key(self):
        self.private_key = self.pfx.GetPrivateKey(0)
        ms = self.pfx.get_LastMethodSuccess()
        if not ms:
            self.last_error = self.pfx.lastErrorText()
        return ms

    def load_rsa(self):
        # Import the private key into the RSA component:
        ms = self.rsa.ImportPrivateKey(self.private_key)
        if not ms:
            self.last_error = self.rsa.lastErrorText()
        else:
            # This example will sign a string, and receive the signature
            # in a base64-encoded string.  Therefore, set the encoding mode
            # to "base64":
            self.rsa.put_EncodingMode(self.encoding_mode)
            # If some other non-Chilkat application or web service is going to be verifying
            # the signature, it is important to match the byte-ordering.
            # The LittleEndian property may be set to True
            # for little-endian byte ordering,
            # or False  for big-endian byte ordering.
            # Microsoft apps typically use little-endian, while
            # OpenSSL and other services (such as Amazon CloudFront)
            # use big-endian.
            self.rsa.put_LittleEndian(self.little_endian)
        return ms
