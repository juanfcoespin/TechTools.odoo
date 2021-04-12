# -*- coding: utf-8 -*-
{
    'name': "TechTools - Configuraciones",

    'summary': """
        Configuraciones en datos maestros""",

    'description': """
        Inventario: 
            - Actualiza los costos de los productos que están en cero al ultimo precio de compra
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Configuracion',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock_account', 'purchase_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/inventario_conf_view.xml',
        "security/ir.model.access.csv",
    ],
}
