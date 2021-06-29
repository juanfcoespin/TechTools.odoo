# -*- coding: utf-8 -*-
{
    'name': "TechTools - Inventario",

    'summary': """
        Desarrollos sobre inventario
        """,

    'description': """
        - que aparezca la factura de venta correspondiente al movimiento de stock en el maestro del producto
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Inventario',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_move.xml',
        'views/product_template.xml',
    ],
    'application': True,
    # only loaded in demonstration mode

}
