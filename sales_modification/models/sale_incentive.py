# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

    maximum_bonus = fields.Float(string="Maximum Bonus")
    brands_objective = fields.Integer(string="N° Brands with Objectives", compute='_compute_count_brands')
    bonus_x_boxes = fields.Float(string="Bonus for Boxes")
    bonus_x_bs = fields.Float(string="Bonus for Bs")
    bonus_x_qualitative = fields.Float(string="Bonus for Qualitative")
    bonus_brand_boxes = fields.Float(string="Bonus for Box Brands", compute='calculate_incentive')
    maximum_charge = fields.Float(string="Maximum % To Charge")

    
    bonus_x_boxes_total = fields.Float(compute='_compute_bonus_x_boxes_total')
    bonus_x_bs_total = fields.Float(compute='_compute_bonus_x_bs_total')
    bonus_x_qualitative_total = fields.Float(compute='_compute_bonus_x_qualitative_total')
    bonus_brand_boxes_total = fields.Float(compute='_compute_bonus_brand_boxes_total')
    maximum_charge_total = fields.Float(compute='_compute_maximum_charge_total')


    def calculate_incentive(self):
        self.bonus_x_boxes_total = self.maximum_bonus * self.bonus_x_boxes / 100
        self.bonus_x_bs_total = self.maximum_bonus * self.bonus_x_bs / 100
        if self.bonus_x_boxes_total and self.brands_objective:
            self.bonus_brand_boxes = self.bonus_x_boxes_total / self.brands_objective

    @api.depends('month','year')
    def _compute_month_year(self):
        month = dict(self._fields['month'].selection).get(self.month)
        year = self.year

        print("Mess: " + str(month) +" " +"Yearr: "+str(year))
        if(month  and year ):
            self.month_year =   f"{month} {year}"
        elif(month):
            self.month_year =   f"{month}"
        else:
            self.month_year = f"{year}"

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
    achievement_in_box = fields.Float(string="Achievement in Boxes", compute='brand_calculation')  # logro en Cajas
    tobe_charged_for_box = fields.Float(string="To be charged for boxes", compute='brand_calculation')  # A cobrar por cajas
    charged_for_box = fields.Float(string="Charge for boxes", compute='brand_calculation')  # Cobra por cajas

    @api.onchange('brand')
    def onchange_brand(self):
        for rec in self:
            if rec.brand:
                rec.code = rec.brand.code

    def brand_calculation(self):
        for rec in self:
            rec.achievement_in_box = rec.sale_by_box / rec.cupor_for_boxes
            rec.tobe_charged_for_box = rec.sale_by_box / rec.cupor_for_boxes
            rec.charged_for_box = rec.sale_incentive_id.bonus_brand_boxes * rec.tobe_charged_for_box


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
