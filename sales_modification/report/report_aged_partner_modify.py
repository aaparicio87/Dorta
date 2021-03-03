# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportAgedPartnerBalance(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_agedpartnerbalance'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed. (Aged Partner Balance)"))

        total = []
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

        target_move = data['form'].get('target_move', 'all')
        date_from = data['form'].get('date_from', time.strftime('%Y-%m-%d'))

        if data['form']['result_selection'] == 'customer':
            account_type = ['receivable']
        elif data['form']['result_selection'] == 'supplier':
            account_type = ['payable']
        else:
            account_type = ['payable', 'receivable']

        if self.env.context.get('from_scheduler'):
            # Convert into string of 'date_from'.
            date_from = date_from.strftime('%Y-%m-%d')

        movelines, total, dummy = self._get_partner_move_lines(account_type, date_from, target_move,
                                                               data['form']['period_length'])
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_partner_lines': movelines,
            'get_direction': total,
        }
