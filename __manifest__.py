{
    'name': "Refund",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'website', 'mail'],
    'data': [
        'data/activity.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/security_rule.xml',
        'views/refund_form.xml',
        'views/refund_record_view.xml',
        'views/refund_payment_details.xml',
        # 'views/activities.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'Refund/static/src/js/submitt_button.js'],
    },

    'demo': [],
    'summary': "logic_refund",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}
