# -*- coding: utf-8 -*-
{
    'name': "Techtools - Factura Electrónica",

    'summary': """
        Facturación electrónica según los lineamientos del SRI
          
    """,

    'description': """
        Funcionalidades:
        07Abr2021:
        - Oculta botones de iteracción con el SRI para factura de proveedores
        - Bloquea la gestión de secuenciales, y claves de acceso para factura de proveedores
        - Guía de Remisión 
        
        Mar2021:
        - Firma electronicamente XMLs de rides
        - Genera layouts de impresion para factura y guia de remisión
        - Envía XML de facturas al SRI en ambiente de pruebas y producción
         
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Facturacion Electronica',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'account', 'tt_company'],

    # always loaded
    'data': [
        'views/stock_picking.xml',
        'views/account.move.xml',
        'views/impuesto.xml',
        'data/fec_email_template.xml',
        'data/fec_send_invoices_cron.xml',
    ],
    'application': True,
}
