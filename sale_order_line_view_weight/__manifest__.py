# -*- coding: utf-8 -*-
{
    'name': "Ver Atributo Peso en la linea de la orden de venta",

    'summary': """
        Ver Atributo Peso en la linea de la orden de venta
        """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'TechTools Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        "views/sale_order_line_view.xml",
    ],
}

