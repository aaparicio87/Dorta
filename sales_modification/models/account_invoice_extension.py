# -*- coding: utf-8 -*-

import base64
from datetime import timedelta
from odoo import models, fields, api


class AccountInvoiceExtension(models.Model):
    _inherit = 'account.invoice'

    payment_activities_line_ids = fields.One2many('payment.activities', 'account_invoice_id',
                                                  string='Payment Activities Lines')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Dispatched'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'In Payment' status is used when payments have been registered for the entirety of the invoice in a journal configured to post entries at bank reconciliation only, and some of them haven't been reconciled with a bank statement line yet.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")

    @api.model
    def default_get(self, default_fields):
        res = super(AccountInvoiceExtension, self).default_get(default_fields)
        context = self._context
        vals = []
        if context.get('active_model') == 'sale.order':
            so = self.env[context.get('active_model')].search([('id', '=', context.get('active_id'))])
            for inv in so.invoice_ids:
                payment_activities_line_ids = {'sale_order': so.name, 'account_invoice_id': self.id,
                                               'account_invoices': inv.number, 'date': inv.date_invoice,
                                               'price_subtotal': inv.amount_total,
                                               'state': dict(inv._fields['state'].selection).get(inv.state)}
                vals.append((0, 0, payment_activities_line_ids))
            res.update({'payment_activities_line_ids': vals})
        return res

    @api.multi
    def pending_invoice_reminder(self):
        """ The Scheduler:
        Send email to Salesperson of Aged Partner Balance report.
        :return:
        """
        template = self.env.ref('sales_modification.salesperson_email_template')
        pai = self.search([('state', 'in', ('draft', 'open'))])
        today = fields.datetime.now().date()
        local_context_user_sec = self.env.context.copy()
        list_salesperson = list(dict.fromkeys([pai_rec.user_id for pai_rec in pai]))
        for res in list_salesperson:
            if res.partner_id.payment_deadline:
                if res.partner_id.deadline_last_send:
                    if today >= res.partner_id.deadline_last_send:
                        template.email_to = res.partner_id.email
                        # data: prepared dict for creating Aged Partner Balance(account.aged.trial.balance).
                        data = {'period_length': 30, 'date_from': today, 'result_selection': 'customer_supplier',
                                'target_move': 'all', 'company_id': 1, 'date_to': False}
                        aged_trail_balance_id = self.env['account.aged.trial.balance'].create(data)
                        # print_data: Prepared a format of Printable report.
                        print_data = {
                            'form': {'date_from': today, 'target_move': 'all', 'result_selection': 'customer_supplier',
                                     'period_length': 30,
                                     'used_context': {'journal_ids': False, 'state': 'all',
                                                      'date_from': today, 'date_to': False,
                                                      'strict_range': True, 'company_id': 1, 'lang': res.partner_id.lang}}}
                        action = aged_trail_balance_id._print_report(print_data)
                        # render_data: For final data format to render report.
                        render_data = action.get('data')
                        local_context_user_sec.update({
                            'name': res.partner_id.name,
                            'from_scheduler': True,
                            'landscape': True,
                            'active_model': 'account.aged.trial.balance',
                            'active_id': aged_trail_balance_id.id,
                            'lang': res.partner_id.lang,
                        })
                        pdf = self.env.ref('accounting_pdf_reports.action_report_aged_partner_balance').with_context(
                            local_context_user_sec).render_qweb_pdf(aged_trail_balance_id.id, render_data)
                        b64_pdf = base64.b64encode(pdf[0])  # convert binary to pdf
                        file_name = "Aged Partner Balance"
                        attachment_id = self.env['ir.attachment'].create({
                            'name': file_name,
                            'type': 'binary',
                            'datas': b64_pdf,
                            'datas_fname': file_name + '.pdf',
                            'store_fname': file_name,
                            'res_model': 'account.aged.trial.balance',
                            'res_id': aged_trail_balance_id.id,
                            'mimetype': 'application/x-pdf'
                        })  # create attachment
                        template.attachment_ids = [(4, attachment_id.id)]  # add attachment in email template.
                        template.with_context(local_context_user_sec).send_mail(self.id, force_send=True,
                                                                                raise_exception=True)
                        template.attachment_ids = [(2, attachment_id.id)]
                        # set date in deadline_last_send after 15 days
                        res.partner_id.deadline_last_send = today + timedelta(days=res.partner_id.payment_deadline)
                if not res.partner_id.deadline_last_send:
                    template.email_to = res.partner_id.email
                    # data: prepared dict for creating Aged Partner Balance(account.aged.trial.balance).
                    data = {'period_length': 30, 'date_from': today, 'result_selection': 'customer_supplier',
                            'target_move': 'all', 'company_id': 1, 'date_to': False}
                    aged_trail_balance_id = self.env['account.aged.trial.balance'].create(data)
                    # print_data: Prepared a format of Printable report.
                    print_data = {
                        'form': {'date_from': today, 'target_move': 'all', 'result_selection': 'customer_supplier',
                                 'period_length': 30,
                                 'used_context': {'journal_ids': False, 'state': 'all',
                                                  'date_from': today, 'date_to': False,
                                                  'strict_range': True, 'company_id': 1, 'lang': res.partner_id.lang}}}
                    action = aged_trail_balance_id._print_report(print_data)
                    # render_data: For final data format to render report.
                    render_data = action.get('data')
                    local_context_user_sec.update({
                        'name': res.partner_id.name,
                        'from_scheduler': True,
                        'landscape': True,
                        'active_model': 'account.aged.trial.balance',
                        'active_id': aged_trail_balance_id.id,
                        'lang': res.partner_id.lang,
                    })
                    pdf = self.env.ref('accounting_pdf_reports.action_report_aged_partner_balance').with_context(
                        local_context_user_sec).render_qweb_pdf(aged_trail_balance_id.id, render_data)
                    b64_pdf = base64.b64encode(pdf[0])  # convert binary to pdf
                    file_name = "Aged Partner Balance"
                    attachment_id = self.env['ir.attachment'].create({
                        'name': file_name,
                        'type': 'binary',
                        'datas': b64_pdf,
                        'datas_fname': file_name + '.pdf',
                        'store_fname': file_name,
                        'res_model': 'account.aged.trial.balance',
                        'res_id': aged_trail_balance_id.id,
                        'mimetype': 'application/x-pdf'
                    })  # create attachment
                    template.attachment_ids = [(4, attachment_id.id)]  # add attachment in email template.
                    template.with_context(local_context_user_sec).send_mail(self.id, force_send=True,
                                                                            raise_exception=True)
                    template.attachment_ids = [(2, attachment_id.id)]
                    # set date in deadline_last_send after 15 days
                    res.partner_id.deadline_last_send = today + timedelta(days=res.partner_id.payment_deadline)


class PaymentActivities(models.Model):
    _name = "payment.activities"
    _description = "Payment Activities"

    account_invoice_id = fields.Many2one('account.invoice', string='Invoice Reference', ondelete='cascade', index=True)
    account_invoices = fields.Char(string='Invoice', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    currency_id = fields.Many2one('res.currency', related='account_invoice_id.company_id.currency_id', readonly=True)
    price_subtotal = fields.Monetary(string='Amount', readonly=True)
    sale_order = fields.Char(string="Sale Order", readonly=True)
    state = fields.Char(string="State", readonly=True)
