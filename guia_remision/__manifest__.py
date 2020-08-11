# -*- coding: utf-8 -*-
{
    'name': "guia_remision",

    'summary': """
        - Construye el RIDE de la guia de remisión conforme a los lineamientos del SRI   
    """,

    'description': """
        Long description of module's purpose
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Facturacion Electronica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/stock_picking.xml',
        'report/guia_remision_report.xml',
        'report/ride.xml'
    ]
}
