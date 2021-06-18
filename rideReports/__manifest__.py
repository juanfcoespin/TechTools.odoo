# -*- coding: utf-8 -*-
{
    'name': "rideReports",

    'summary': """
        Reporte de los RIDES  de facturación electrónica según los lineamientos del SRI
          
    """,

    'description': """
        - Guía de Remisión 
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Facturacion Electronica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'account', 'rides'],

    # always loaded
    'data': [
        'report/custom_header.xml',
        'report/rides.xml',
        'report/factura_ride.xml',
        'report/guia_remision_ride.xml',
    ],
    'application': True,
}
