import base64
import os
from os import path


def remove_chars(chars_to_remove, str_in):
    for char in chars_to_remove:
        str_in = str_in.replace(char, '')
    return str_in


def create_file_from_binary(binary, file_path, decode_to64=False):
    buffer = open(file_path, "wb")
    if decode_to64:
        buffer.write(base64.b64decode(binary))
    else:
        buffer.write(binary)
    buffer.close()


def get_pdf_report_binary(self, report_name):
    report = self.env['ir.actions.report']._get_report_from_name(report_name)
    pdf = report._render_qweb_pdf(self.id)
    return pdf[0]


def get_ride_path(self, subfolder_name, file_name=None):
    ride_path = self.company_id.electronic_docs_path
    if ride_path is None:
        raise Exception('Debe configurar la ruta de destino de los rides')
    ride_path = os.path.join(ride_path, subfolder_name)
    if not path.exists(ride_path):
        try:
            os.mkdir(ride_path)
            if file_name is not None:
                ride_path = os.path.join(ride_path, file_name)
            return ride_path
        except OSError:
            raise Exception('no se pudo crear el directorio: ' + ride_path)
            return None
