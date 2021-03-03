from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrderPopup(models.TransientModel):
    _name = 'sale.order.popup'

    @api.multi
    def popup_button(self):
        for rec in self.env['sale.order'].browse(self._context.get('active_id')):
            if rec._get_forbidden_state_confirm() & set(rec.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                ) % (', '.join(rec._get_forbidden_state_confirm())))

            for order in rec.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            rec.write({
                'state': 'sale',
                'confirmation_date': fields.Datetime.now()
            })
            rec._action_confirm()
            if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                rec.action_done()

        return True

class Quotation_Send_Popup(models.TransientModel):
    _name = 'quotation.send.popup'

    @api.multi
    def action_quotation_send_popup(self):
        for rec in self.env['sale.order'].browse(self._context.get('active_id')):
            ir_model_data = self.env['ir.model.data']
            try:
                template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
            except ValueError:
                template_id = False
            try:
                compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
            except ValueError:
                compose_form_id = False
            lang = rec.env.context.get('lang')
            template = template_id and self.env['mail.template'].browse(template_id)
            if template and template.lang:
                lang = template._render_template(template.lang, 'sale.order', rec.ids[0])
            ctx = {
                'default_model': 'sale.order',
                'default_res_id': rec.ids[0],
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'mark_so_as_sent': True,
                'model_description': rec.with_context(lang=lang).type_name,
                'custom_layout': "mail.mail_notification_paynow",
                'proforma': rec.env.context.get('proforma', False),
                'force_email': True
            }
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context': ctx,
            }

        return True