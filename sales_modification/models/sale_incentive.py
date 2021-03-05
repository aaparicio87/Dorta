# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions

def get_years():
    year_list = []
    for i in range(2016, 2036):
        year_list.append((i, str(i)))
    return year_list


class SaleIncentive(models.Model):
    _name = 'sale.incentive'
    _description = "Sale Incentive"
    _rec_name = "region"

    region = fields.Many2one('region.incentive', string="Region")
    seller = fields.Many2one('res.partner', string="Seller")
    supervisor = fields.Many2one('res.partner', string="Supervisor")
    is_supervisor = fields.Boolean()
    is_seller = fields.Boolean()
    total_region = fields.Many2many('res.country', string="Total region")
    month = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                              (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                              (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], string='Month')
    year = fields.Selection(get_years(), string='Year')
    bonuses_id = fields.Many2one('sale.bonuses', string="Maximum Bonus")  # Bono Maximo
    brand_line_objectives_ids = fields.One2many('brand.objectives', "sale_incentive_id",
                                                string="Brand Lines with Objectives")
    state = fields.Selection(
        [('incentive_reg', 'Incentive Registration'),
         ('incentive_sent', 'Incentive Sent'),
         ('incentive_approved', 'Incentive Approved'),
         ], string='State', default='incentive_reg')

    month_year = fields.Char(string='Month/Year', compute='_compute_month_year')

    brands_objective = fields.Integer(string="N° Brands with Objectives")
    maximum_bonus = fields.Float(string='Maximum Bonus', digits=(12, 6))
    bonus_x_boxes = fields.Many2one('sale.bonuses', string='Bonus for Boxes')
    bonus_x_bs = fields.Many2one('sale.bonuses', string='Bonus for Bs')
    bonus_x_qualitative = fields.Many2one('sale.bonuses', string='Bonus for Qualitative')
    bonus_brand_boxes = fields.Float(string='Bonus for Box Brands', digits=(12, 6))
    maximum_charge = fields.Float(string='Maximum % To Charge',  digits=(12, 6))

    bonus_x_boxes_total = fields.Float()
    bonus_x_bs_total = fields.Float()
    bonus_x_qualitative_total = fields.Float()

    total_cupor_for_boxes = fields.Float(string="Total Coupon for boxes") # Total Cupor by box
    total_space_in_bs = fields.Float(string="Total Coupon in Bs")  # Total Cupo in Bs
    total_sale_by_box = fields.Float(string="Total Sale by Boxes")  # Total Sales by Box
    total_sale_in_bs = fields.Float(string="Total Sale in Bs.")  # Total Sales in BS
    total_charged_by_box = fields.Float(string="Total Charge by Box.")  # Total Charge by Box

    achievement_percent = fields.Float(string="% Achievement")
    achievement_to_collect_percent = fields.Float(string="% Achievement to Collet")
    incentive_bs = fields.Float(string="Incentive in BS")
    incentive_x_box = fields.Float(string="Incentive by Box")
    total_incentive = fields.Float(string="Total Incentive")

    @api.onchange('supervisor')
    def _is_supervisor(self):
        print("aaaaaa"+str(self.supervisor.id))
        if self.supervisor:
            self.is_supervisor = True

    @api.onchange('seller')
    def _is_seller(self):
        if self.seller:
            self.is_seller = True

    @api.onchange('brand_line_objectives_ids')
    def count(self):
        bo = len(self.mapped('brand_line_objectives_ids'))
        self.brands_objective = bo

    @api.depends('month','year')
    def _compute_month_year(self):
        for rec in self:
            month_sel = dict(rec._fields['month'].selection).get(rec.month)
            year_sel = rec.year

            if(month_sel  and year_sel):
                rec.month_year = f"{month_sel} {year_sel}"
            elif(month):
                rec.month_year = f"{month_sel}"
            else:
                rec.month_year = f"{year_sel}"
    
    @api.onchange('bonus_x_boxes')
    def calc_bonus_x_boxes_total(self):
        mb = self.maximum_bonus
        amount = self.bonus_x_boxes.amount/100

        if(mb == 0 and amount > 0):
            return{
                'warning':{
                    'title':'Maximum Bonus not typed',
                    'message':'Maximum Bonus must be typed'
                }
            }
        else:
            self.bonus_x_boxes_total = mb * amount
    
    @api.onchange('bonus_x_bs')
    def calc_bonus_x_bs_total(self):
        mb = self.maximum_bonus
        amount = self.bonus_x_bs.amount/100

        if(mb == 0 and amount > 0):
            return{
                'warning':{
                    'title':'Maximum Bonus not typed',
                    'message':'Maximum Bonus must be typed'
                }
            }
        else:
            self.bonus_x_bs_total = mb * amount

    @api.onchange('bonus_x_qualitative')
    def calc_bonus_x_qualitative_total(self):
        mb = self.maximum_bonus
        amount = self.bonus_x_qualitative.amount/100

        if(mb == 0 and amount > 0):
            return{
                'warning':{
                    'title':'Maximum Bonus not typed',
                    'message':'Maximum Bonus must be typed'
                }
            }
        else:
            self.bonus_x_qualitative_total = mb * amount

    @api.onchange('brand_line_objectives_ids')
    def calc_bonus_brand_boxes(self):
        if len(self.mapped('brand_line_objectives_ids')) > 0:
            if self.brands_objective > 0:
                self.bonus_brand_boxes = self.maximum_bonus/self.brands_objective
                

    @api.onchange('brand_line_objectives_ids')
    def totals_lines_objectives(self):
        if len(self.mapped('brand_line_objectives_ids')) > 0:
            for rec in self.mapped('brand_line_objectives_ids'):
                self.total_cupor_for_boxes = self.total_cupor_for_boxes + rec.cupor_for_boxes
                self.total_space_in_bs = self.total_space_in_bs + rec.space_in_bs
                self.total_sale_by_box = self.total_sale_by_box + rec.sale_by_box
                self.total_sale_in_bs = self.total_sale_in_bs + rec.sale_in_bs
                self.total_charged_by_box = self.total_charged_by_box + rec.charged_for_box

                if self.total_space_in_bs > 0:
                    self.achievement_percent = self.total_sale_in_bs/(self.total_space_in_bs * 100)
                    self.achievement_to_collect_percent = self.achievement_percent

                self.incentive_bs = self.achievement_to_collect_percent * self.bonus_x_bs_total
                self.incentive_x_box = self.total_charged_by_box
                self.total_incentive = self.incentive_bs + self.incentive_x_box
            
class BrandObjectives(models.Model):
    _name = "brand.objectives"
    _description = "Brand Objectives"

    sale_incentive_id = fields.Many2one('sale.incentive', string='Sale Incentive')
    brand = fields.Many2one('brand.code', string="Brand")  # Marca
    code = fields.Char(string="code")  # Codigo
    description = fields.Char(string="Description")
    cupor_for_boxes = fields.Float(string="Cupor for boxes")  # Cupor por cajas
    space_in_bs = fields.Float(string="Space in Bs")  # Cupo en Bs
    sale_by_box = fields.Float(string="Sale by Boxes")  # Venta por Cajas
    sale_in_bs = fields.Float(string="Sale in Bs.")  # Venta en Bs
    achievement_in_box = fields.Float(string="Achievement in Boxes", compute='_compute_achievement_in_box')  # logro en Cajas
    tobe_charged_for_box = fields.Float(string="To be charged for boxes", compute='_compute_tobe_charged_for_box')  # A cobrar por cajas
    charged_for_box = fields.Float(string="Charge for boxes", compute='_compute_charged_for_box')  # Cobra por cajas

    @api.onchange('brand')
    def onchange_brand(self):
        for rec in self:
            if rec.brand:
                rec.code = rec.brand.code

    @api.depends('sale_by_box','cupor_for_boxes')
    def _compute_achievement_in_box(self):
        for rec in self:
            if rec.cupor_for_boxes > 0:
                rec.achievement_in_box = rec.sale_by_box / rec.cupor_for_boxes
           

    @api.depends('achievement_in_box')
    def _compute_tobe_charged_for_box(self):
        for rec in self:
            rec.tobe_charged_for_box = rec.achievement_in_box

    @api.depends('sale_incentive_id','tobe_charged_for_box')
    def _compute_charged_for_box(self):
        for rec in self:
            rec.charged_for_box = rec.tobe_charged_for_box * rec.sale_incentive_id.bonus_brand_boxes

class BrandCode(models.Model):
    _name = "brand.code"
    _rec_name = 'brand'

    code = fields.Char(string="Code")
    brand = fields.Char(string="Brand")  # Marca


class Region(models.Model):
    _name = "region.incentive"
    _rec_name = 'name'

    code = fields.Char(string="Code")
    name = fields.Char(string="Region")
