# -*- coding: utf-8 -*-
{
    'name': "rides",

    'summary': """
        Construye los RIDES  de facturación electrónica según los lineamientos del SRI
          
    """,

    'description': """
        - Guía de Remisión 
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Facturacion Electronica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'account'],

    # always loaded
    'data': [
        'views/stock_picking.xml',
        'views/account.move.xml',
        'report/custom_header.xml',
        'report/rides.xml',
    ]
}
