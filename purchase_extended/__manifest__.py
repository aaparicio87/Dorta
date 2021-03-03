{
    'name': "Purchase extended",
    'version': '12.0.0',
    'author': "MP Technolabs",
    'website': "https://www.mptechnolabs.com",
    'summary': "",
    'description': "",
    'depends': ['base_vat', 'purchase', 'stock'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/product_template.xml',
        'views/document_document.xml',
        'views/custom_control.xml',
        'views/purchase_view.xml',
        'views/account_invoice.xml',
        'views/price_list.xml',
        'views/purchase_custom.xml',
        'views/shopping_program.xml',
        'data/cron.xml',
        'data/shopping_program_mail.xml',
        'reports/shopping_program_report.xml'
    ],
    'installable': True,
    'application': True,
}
