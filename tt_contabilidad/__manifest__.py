# -*- coding: utf-8 -*-
{
    'name': "TechTools - Contabilidad",

    'summary': """
        Contabilidad Ecuador""",

    'description': """
        - Establece el plan de cuentas para ecuador
    """,

    'author': "TechTools",
    'website': "http://www.techtoolsec.com",
    'category': 'Contabilidad',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/account.account2.csv',
    ],

}
