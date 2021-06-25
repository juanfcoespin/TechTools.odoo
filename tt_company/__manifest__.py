# -*- coding: utf-8 -*-
{
    'name': "TechTools - Compañia",

    'summary': """
        Extensión de funcionalidad en la compañia""",

    'description': """
        Extensión de funcionalidad en la compañia
        
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Compañía',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "security/ir.model.access.csv",
        'views/res_company_ec.xml',
        'data/punto_emision_template.xml',
    ],
    'application': True,
}
