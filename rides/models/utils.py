from datetime import datetime

def kg_to_quintales(kg):
    ms = kg / 46.008
    return round(ms, 2)


def get_num_ride(company, number):
    # 145 -> '000000145'
    secuencial = str(number).rjust(9, '0')
    return "{}-{}-{}".format(company.cod_establecimiento,
                             company.cod_punto_emision, secuencial)

def get_clave_acceso():
    today = datetime.today()
    current_date = "{}{}{}".format(str(today.day).rjust(2, '0'),
                                   str(today.month).rjust(2, '0'), today.year)
    return current_date


