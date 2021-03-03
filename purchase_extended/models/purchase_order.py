from odoo import api, fields, models, _


class purchase_order(models.Model):
    _inherit = "purchase.order"

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        res = super(purchase_order, self).onchange_partner_id()
        if self.partner_id.text_note:
            self.notes = self.partner_id.text_note
        return res

    @api.multi
    def open_custom_control(self):

        form_id = self.env.ref('purchase_extended.view_custom_control_inherit').id
        status = ''
        if self.state == 'purchase':
            status = 'paid'
        else:
            self.state == 'draft'
            status = 'draft'
        return {
            'type': 'ir.actions.act_window',
            'name': _('Custom Control'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.control',
            'views': [(form_id, 'form')],
            'context': {
                'default_purchase_order_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_status_order': self.state,
                'default_state': status,
                'default_issue_date': self.date_order,
            }
        }