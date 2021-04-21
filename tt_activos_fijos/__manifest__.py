# -*- coding: utf-8 -*-
{
    'name': "TechTools - Activos Fijos",

    'summary': """
        Gestión de activos fijos""",

    'description': """
        - Asignacion de custodios
        - Depreciación
        - Actas Entrega recepción de activos
        - Trasabilidad de custodios
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Inventario',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/activo_view.xml',
        "security/ir.model.access.csv",
        'data/secuence.xml',
    ]
}
