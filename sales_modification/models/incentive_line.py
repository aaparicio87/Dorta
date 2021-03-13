# -*- coding: utf-8 -*-

from odoo import api, fields, models

def get_years():
    year_list = []
    for i in range(2016, 2036):
        year_list.append((i, str(i)))
    return year_list

class IncentiveLine(models.Model):
    _name = 'incentive.line'
    _description = 'Report for incentive'

    sale_incentive_id        = fields.Many2one('sale.incentive', string='Sale Incentive')
    incentive_by_box         = fields.Float(string="Incentive by Box", compute='_compute_incentive_by_box', store=True)
    maximum_bonus            = fields.Float(string = "Cap assigned by sales team", compute='_compute_maximum_bonus', store=True)
    cupor_for_boxes          = fields.Float(string = "Goal assigned per month", compute='_compute_cupor_for_boxes', store=True)
    space_in_bs              = fields.Float(string = "Target by product price list", compute='_compute_space_in_bs', store=True)  
    incentive_by_seller      = fields.Float(string = "By seller", compute='_compute_incentive_by_seller', store=True)   
    incentive_by_supervisor  = fields.Float(string = "By supervisor", compute='_compute_incentive_by_supervisor', store=True)

    region                    = fields.Many2one('region.incentive', string="Region", domain="[('sale_incentive_id', '=?', sale_incentive_id)]")
    seller                    = fields.Many2one('res.partner', string="Seller", domain="[('id', '=', sale_incentive_id.seller.id)]")
    supervisor                = fields.Many2one('res.partner', string="Supervisor", domain="[('id', '=', sale_incentive_id.supervisor.id)]")
    month                     = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                              (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                              (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], string='Month') 
    year                      = fields.Selection(get_years(), string='Year')


    @api.depends('sale_incentive_id')
    def _compute_incentive_by_box(self):
        criteria = [('id', '=', self.sale_incentive_id.id)]
        incentive = self.env['sale.incentive'].search(criteria)

        for rec in incentive:
            return rec.incentive_x_box

    @api.depends('sale_incentive_id')
    def _compute_maximum_bonus(self):
        criteria = [('id', '=', self.sale_incentive_id.id)]
        incentive = self.env['sale.incentive'].search(criteria)

        for rec in incentive:
            return rec.maximum_bonus.amount

    @api.depends('sale_incentive_id')
    def _compute_cupor_for_boxes(self):
        criteria = [('id', '=', self.sale_incentive_id.id)]
        incentive = self.env['sale.incentive'].search(criteria)

        for rec in incentive:
            return rec.incentive_x_box
    
    @api.depends('sale_incentive_id')
    def _compute_space_in_bs(self):
        criteria = [('id', '=', self.sale_incentive_id.id)]
        incentive = self.env['sale.incentive'].search(criteria)

        for rec in incentive:
            return rec.incentive_bs
    
    @api.depends('sale_incentive_id')
    def _compute_incentive_by_seller(self):
        criteria = [('id', '=', self.sale_incentive_id.id),('is_seller','=',True)]
        incentive = self.env['sale.incentive'].search(criteria)

        for rec in incentive:
            return rec.total_incentive

    @api.depends('sale_incentive_id')
    def _compute_incentive_by_supervisor(self):
        criteria = [('id', '=', self.sale_incentive_id.id),('is_supervisor','=',True)]
        incentive = self.env['sale.incentive'].search(criteria)

        for rec in incentive:
            return rec.total_incentive