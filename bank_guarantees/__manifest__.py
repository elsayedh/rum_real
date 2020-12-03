# -*- coding: utf-8 -*-
{
    'name': "Bank Guarantees",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/bank_customer_guarantees.xml',
        'views/bank_vendor_guarantees.xml',
        'views/templates.xml',
        'views/guarantee_customer_report_report.xml',
        'views/guarantee_customer_report.xml',
        'views/guarantee_vendor_report_report.xml',
        'views/guarantee_vendor_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
