# Copyright 2019
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Administración",
    'summary': """
        Facturas y Pagos / DORTA""",
    'author': "Odoo Community Association (OCA)",
    'website': "https://www.softnetcorp.net",
    'category': 'Accounting/Accounting',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'depends': ['account'],
    'data': ['security/invoice_hide_analytic_column.xml',
             'views/invoice_modification_hide_analytic_column.xml',
             'views/invoice_modification_account_payment_form.xml',
             'views/invoice_modification_crm_team_view.xml'],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
