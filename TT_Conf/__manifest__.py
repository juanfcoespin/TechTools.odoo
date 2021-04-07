# -*- coding: utf-8 -*-
{
    'name': "TechTools - Ajustes",

    'summary': """
        modulo para gestionar ajustes de maestros """,

    'description': """
        
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Facturacion Electronica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'report/guia_remision_report.xml',
    ],
}
