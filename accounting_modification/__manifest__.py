# -*- coding: utf-8 -*-

{
    'name': "Accounting Modification",

    'summary': """
        Account Modification / Account Extend""",

    'description': """
        Account Modification / Account Extend.
    """,

    'author': "MP Technolabs",
    'website': "https://www.mptechnolabs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing Management',
    'version': '12.0.1.4',

    # any module necessary for this one to work correctly
    'depends': ['accounting_pdf_reports', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice_modifiy_views.xml',
        'views/sale_views_inherit.xml',
        'views/res_partner_view.xml',
        'views/company_view.xml',
        'views/product_view_inherit.xml',
        'report/account_invoice_report.xml',
        'wizard/liquor_book_report_template.xml',
        'wizard/liquor_book_report.xml'
    ],
}
