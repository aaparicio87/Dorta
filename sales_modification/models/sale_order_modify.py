# -*- coding: utf-8 -*-
from datetime import date, datetime

from odoo import fields, models, api, _

from odoo.exceptions import ValidationError,UserError


class SaleOrderModify(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def check_pending_payment(self):
        """
        Check pending Sale Order of selected partner.
        If pending then show an error massage.
        Else :return: True
        """
        user_id = self.env.user
        if user_id.id:
            so = self.env['sale.order'].search(
                [('partner_id', '=', self.partner_id.id), ('state', 'in', ['draft', 'sent'])])
            if so:
                so_names = ""
                for rec in so:
                    so_names = so_names + rec.name + ", "
                msg1 = _('You Can Not Confirm This Sale Order.')
                msg2 = _("Customer has pending orders. i.e ") + str(so_names)
                msg3 = _("Please check with Supervisor.")
                raise UserError(msg1 + '\n' + msg2 + '\n' + msg3)
        return True

    @api.multi
    def check_overduebills(self):
        """
        Check pending Invoices selected partner.
        If pending then show an error massage.
        Else :return: True
        """
        user_id = self.env.user
        if user_id.id:
            ai = self.env['account.invoice'].search(
                [('partner_id', '=', self.partner_id.id), ('state', 'in', ['draft', 'open'])])
            if ai:
                ai_names = ""
                for rec in ai:
                    if rec.number:
                        ai_names = ai_names + rec.number + ", "
                    else:
                        pass
                msg1 = _('You can not confirm this Sale Order.')
                msg2 = _("Customer has due invoices.") + str(ai_names)
                msg3 = _("Please check with Supervisor.")
                raise UserError(msg1 + '\n' + msg2 + '\n' + msg3)
        return True

    @api.multi
    def check_inventory(self):
        """
        To check Qty available for product or not.
        :return:
        """
        user_id = self.env.user
        if user_id.id:
            for rec in self.order_line:
                if float(rec.product_id.qty_available) <= 0.0:
                    msg1 = _('Qty of ')
                    msg2 = _(' is ')
                    msg3 = _('.\n You can not proceed. Please check with Supervisor.')
                    raise UserError(msg1 + str(rec.product_id.name) + msg2 + str(rec.product_id.qty_available) + msg3)
        return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrderModify, self).action_confirm()
        for order in self:
            order.check_pending_payment()
            order.check_overduebills()
            order.check_inventory()
        return res

    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quote Template',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Quote'),
        ('sent', 'Quote Sent'),
        ('sale', 'Sales Order'),
        ('refuse', 'To Refuse'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')
    exchange_rate = fields.Selection([('rate_of_day', 'Rate of Day'), ('manual_rate', 'Manual Rate')],
                                     string="Exchange Rate", default="rate_of_day")
    rate_of_day = fields.Float(string="Rate of Day")
    manual_rate = fields.Float(string="Manual Rate")
    repeat = fields.Boolean(string='Repeat')
    expired_rif = fields.Boolean(string='Expired RIF')
    limit_credit = fields.Boolean(string='Credit limit')
    low_limit_credit = fields.Boolean(string='Low credit limit')
    unavailable_stock = fields.Boolean(string='Unavailable Stock')
    pending_invoice = fields.Boolean(string='Pendign Invoice')
    pending_so_payment = fields.Boolean(string='Pending Sale Order Payment')

    def print_quotations(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        return self.env.ref('sales_modification.action_report_saleorders')\
            .with_context(discard_logo_check=True).report_action(self)


    @api.onchange('pricelist_id')
    def get_rate_of_day(self):
        company_id = self.pricelist_id
        if company_id:
            # rate = company_id.currency_id._get_rates(company_id, fields.Date.today())
            # self.rate_of_day = rate.get(company_id.currency_id.id)
            self.rate_of_day = company_id.currency_id.rate

    @api.onchange('exchange_rate')
    def set_manual_rate(self):
        if self.exchange_rate == 'manual_rate':
            self.manual_rate = self.rate_of_day

    @api.model_create_multi
    def action_to_refuse(self):
        for order in self:
            order.state = 'refuse'

    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        if self.state == 'draft':
            if self.partner_id.rif_valid_date < date.today() and not self.partner_id.user_id.has_group('base.group_system'):
                return {
                    'view_mode': 'form',
                    'res_model': 'quotation.send.popup',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                    'target': 'new',
                }
                # raise ValidationError('RIF Date is Expired')
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        lang = self.env.context.get('lang')
        template = template_id and self.env['mail.template'].browse(template_id)
        if template and template.lang:
            lang = template._render_template(template.lang, 'sale.order', self.ids[0])
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'model_description': self.with_context(lang=lang).type_name,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
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

    @api.multi
    def action_confirm(self):
        if self.state == 'draft':
            if self.partner_id.rif_valid_date < date.today() and not self.partner_id.user_id.has_group('base.group_system'):
                return  {
                    'view_mode': 'form',
                    'res_model': 'sale.order.popup',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                    'target': 'new',
                }

            if self._get_forbidden_state_confirm() & set(self.mapped('state')):
                raise UserError(_(
                    'It is not allowed to confirm an order in the following states: %s'
                ) % (', '.join(self._get_forbidden_state_confirm())))

            for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
                order.message_subscribe([order.partner_id.id])
            self.write({
                'state': 'sale',
                'confirmation_date': fields.Datetime.now()
            })
            self._action_confirm()
            if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
                self.action_done()
        return True
    

    @api.model
    def create(self, values):

        record = super(SaleOrderModify, self).create(values)
        current_date = str(datetime.now().date())
        
        domain = [('partner_id', '=', record.partner_id.id)]
        orders = self.env['sale.order'].search(domain)
        partner = self.env['res.partner'].search([('id','=',record.partner_id.id)])
        active_invoice = self.env['account.invoice'].search(
                [('partner_id', '=', record.partner_id.id), ('state', 'in', ['draft', 'open'])])
        pending_sale_ord = self.env['sale.order'].search(
                [('partner_id', '=', record.partner_id.id), ('state', 'in', ['draft', 'sent'])])
        cont = 0
        cont_rif = 0
        for order in orders:
            date_of_order = str(order.date_order.date())
            if date_of_order == current_date:
                cont = cont + 1
        if cont > 1:
            record.state = 'draft'
            record.repeat = True
        if str(partner.rif_valid_date) <= current_date:
            record.state = 'draft'
            record.expired_rif = True
        if partner.credit_limit < record.amount_total:
            record.state = 'draft'
            record.limit_credit = True
        if record.order_line.product_id.qty_available < record.order_line.product_uom_qty or record.order_line.product_id.qty_available <= 0.0 : 
            record.state = 'draft'
            record.unavailable_stock = True
        if active_invoice:
            record.state = 'draft'
            record.pending_invoice = True
        if pending_sale_ord:
            record.state = 'draft'
            record.pending_so_payment = True
        return record       

class SaleOrderLineModify(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        res = super(SaleOrderLineModify, self)._compute_amount()
        for line in self:
            if line.order_id.pricelist_id.currency_id.id != line.company_id.currency_id.id:
                price_unite = line.price_unit / 100
                price = price_unite * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                                product=line.product_id, partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                    'price_unit': price
                })
            return res
    
    @api.onchange('product_id')
    def unit_price(self):
        if self.product_id:
            if self.order_id.exchange_rate == 'rate_of_day':
                self.price_unit = self.product_id.list_price * self.order_id.rate_of_day
            else:
                self.price_unit = self.product_id.list_price * self.order_id.manual_rate