# pylint: disable=eval-used
# pylint: disable=eval-referenced
# pylint: disable=consider-add-field-help
# pylint: disable=broad-except
# pylint: disable=missing-return

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class AccountInvoice2(models.Model):
    _inherit = ['account.invoice']

    is_group_invoice = fields.Boolean(compute="_compute_is_group_invoice")

    def _compute_is_group_invoice(self):
        grp_fact = self.env['res.groups'].search(
            [('name', 'ilike', 'facturacion')])
        if grp_fact.id in self.env.user.groups_id.ids:
            self.is_group_invoice = True
        else:
            self.is_group_invoice = False


class AccountInvoiceLine2(models.Model):
    _inherit = ['account.invoice.line']

    is_group_invoice_line = fields.Boolean(compute="_compute_is_group_invoice")

    def _compute_is_group_invoice(self):
        self.is_group_invoice_line = self.invoice_id.is_group_invoice


class AccountPaymenti2(models.Model):
    _inherit = 'account.payment'

    entry_date = fields.Date(
        string="Fecha de Pago",
        default=lambda self: fields.Date.context_today(self),
        translate=True)
