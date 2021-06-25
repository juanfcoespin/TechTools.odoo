# -*- coding: utf-8 -*-
{
    'name': "guia_remision",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
        # 'security/ir.model.access.csv',
        "security/ir.model.access.csv",
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        'report/guia_remision_report.xml',
    ],
}
