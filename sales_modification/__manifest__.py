# -*- coding: utf-8 -*-
{
    'name': "Sales Modification(Updated)",
    # sales_modification

    'summary': """
        Sales Modification""",

    'description': """
        Sales Modification / Sales Extension.
    """,

    'author': "MP Technolabs",
    'website': "http://www.mptechnolabs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.3',

    # any module necessary for this one to work correctly
    #'depends': ['sale','sale_management','','base_vat'],
    'depends': ['sale', 'sales_team', 'account', 'base_vat', 'accounting_pdf_reports', 'sale_management', 'purchase'],
    # always loaded
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_pending_invoice_email.xml',
        'data/email_template.xml',
        'data/sale_incentive_sequence.xml',
        'report/sale_report_modify.xml',
        'report/sale_report_inherit.xml',
        'report/incentive_report.xml',
        'wizard/sale_order_popup.xml',
        'views/incentive_view.xml',
        'views/sale_views_modify.xml',
        'views/sale_portal_templates_modify.xml',
        'views/sale_onboarding_views_modify.xml',
        'views/payment_activities_view.xml',
        'views/crm_view.xml',
        'views/sale_bonuses_view.xml',
        'views/res_partner_view_modify.xml'
    ],
}
