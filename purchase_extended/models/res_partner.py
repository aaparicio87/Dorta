from odoo import api, fields, models, _

dispatch_day = [('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'),
                ('6', 'Saturday'), ('7', 'Sunday')]


class res_partner(models.Model):
    _inherit = "res.partner"

    dispatch_day_sale = fields.Selection(dispatch_day, string='Dispatch Day')
    dispatch_day_purchase = fields.Selection(dispatch_day, string='Dispatch Days')
    text_note = fields.Text()
    payment_methods = fields.Many2one('payment.methods', string="Payment Methods")
    wholesaler = fields.Many2one('res.partner', string="Wholesaler")
    key_account = fields.Char(string="Key Account")
    horizontal = fields.Char(string="Horizontal")
    rif_valid_date = fields.Date(string="RIF Valid Date")
    fiscal_address = fields.Text(string="Fiscal Address")
    litrage_id = fields.Many2many('stock.extended.litrage', column1='partner_id',
                                    column2='litrage_id', string='Litrage'
    )

class PaymentMethods(models.Model):
    _name = 'payment.methods'

    name = fields.Char(string="Name")


class Litrage(models.Model):
    _name = "stock.extended.litrage"
    _description = "Litrage"
    _rec_name = "litrage"

    litrage = fields.Float(string='Litrage', digits=(12, 2))

    partner_ids = fields.Many2many('res.partner', column1='litrage_id', column2='partner_id', string='Partners')
    