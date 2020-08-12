# -*- coding: utf-8 -*-
{
    'name': "Socio Negocio Ecuador",

    'summary': """
        Gestion del socio de negocio en ecuador
        """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'TechTools Socio Negocio EC',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "views/res_partner_ec.xml",
        "views/res_company_ec.xml"
    ],
}

