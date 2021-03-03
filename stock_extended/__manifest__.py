{
    'name': "Stock Extended",
    'version': '12.0.0',
    'author': "MP Technolabs",
    'website': "http://www.mptechnolabs.com",
    'summary': "",
    'description': "",
    'depends': ['base','purchase', 'stock'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/stock.xml',
        'views/loading_guides_view.xml',

        'report/loding_guides.xml',
        'report/report_deliveryslip.xml',

    ],
    'installable': True,
    'application': True,
}
