from odoo import api, fields, models, _


class account_invoice(models.Model):
    _inherit = "account.invoice"

    comment = fields.Text(related='partner_id.text_note',string='Additional Information', readonly=True, states={'draft': [('readonly', False)]})