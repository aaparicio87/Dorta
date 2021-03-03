# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountInvoiceModification(models.Model):
    _inherit = "account.invoice"

    sales_team_user_id = fields.Many2one('res.users', string="Líder de Equipo", related="team_id.user_id")

    # @api.multi
    # def _get_report_base_filename(self):
    #     self.ensure_one()
    #     return self.type == 'out_invoice' and self.state == 'draft' and _('Draft Amending Invoice') or \
    #            self.type == 'out_invoice' and self.state in ('open', 'in_payment', 'paid') and _('Invoice - %s') % (
    #                self.number) or \
    #            self.type == 'out_refund' and self.state == 'draft' and _('Credit Note') or \
    #            self.type == 'out_refund' and _('Credit Note - %s') % (self.number) or \
    #            self.type == 'in_invoice' and self.state == 'draft' and _('Vendor Bill') or \
    #            self.type == 'in_invoice' and self.state in ('open', 'in_payment', 'paid') and _('Vendor Bill - %s') % (
    #                self.number) or \
    #            self.type == 'in_refund' and self.state == 'draft' and _('Vendor Credit Note') or \
    #            self.type == 'in_refund' and _('Vendor Credit Note - %s') % (self.number)

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoiceModification, self)._onchange_partner_id()
        if self.partner_id and self.partner_id.note_for_invoice:
            self.comment = self.partner_id.note_for_invoice
        else:
            self.comment = ''
        return res


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection([('draft', 'Borrador'), ('posted', 'Pendiente'), ('sent', 'Enviado'), ('reconciled', 'Reconciliado'),
                              ('cancelled', 'Cancelado')], readonly=True, default='draft', copy=False, string="Status")
    entry_date = fields.Date(string="Fecha de Pago", default=lambda self: fields.Date.context_today(self),
                             translate=True)
    # @api.model
    # def default_get(self, fields):
    #     res = super(AccountPayment, self).default_get(fields)
    #     res['entry_date'] = fields.Date.today()
    #     return res
