# -*- coding: utf-8 -*-

{
    'name': 'Moyasar Payment Acquirer',
    'category': 'Accounting/Payment',
    'summary': 'Payment Acquirer: Moyasar Implementation',
    'version': '1.0',
    'description': """Moyasar Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_moyasar_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    "application"          :  True,
"sequence"             :  1,
}
