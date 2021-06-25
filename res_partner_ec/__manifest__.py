# -*- coding: utf-8 -*-
{
    'name': "Socio Negocio Ecuador",

    'summary': """
        Gestion de socio de negocio en ecuador
        """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Socio Negocio',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/res_partner_ec.xml",
        "views/res_company_ec.xml",
    ],
    'application': True,
}

