# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleBonuses(models.Model):
    _name = 'sale.bonuses'
    _description = "Sale Bonuses"

    name = fields.Char(string="Bond name")
    percentage_scope = fields.Selection([('sale', 'Sales'),
                                         ('purchases', 'Purchases'),
                                         ('incentive', 'Incentive'),
                                         ('none', 'None'),
                                         ('adjustment', 'Adjustment')], string="Percentage scope") #incentive
    calculating_taxes = fields.Many2one('account.tax', string="Calculating taxes") #tax
    amount = fields.Float(string='Amount', digits=(12, 2))
    active = fields.Boolean('Active', default=True,
                            help="If unchecked, it will allow you to disable bonus.")
