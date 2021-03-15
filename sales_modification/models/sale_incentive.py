# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
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

    name = fields.Char(string="Incentive Name", readonly=True, required=True, copy=False, default='New')
    region = fields.Many2one('region.incentive', string="Region")
    seller = fields.Many2one('res.partner', string="Seller")
    supervisor = fields.Many2one('res.partner', string="Supervisor")
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always', track_sequence=1, help="You can find a customer by its Name, TIN, Email or Internal Reference.")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.incentive'))
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)
    sequence_id = fields.Many2one('ir.sequence',
        required=True,
    )
    is_supervisor = fields.Boolean()
    is_seller = fields.Boolean()
    total_region = fields.Many2many('res.country', string="Total region")
    month = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                              (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                              (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], string='Month')
    year = fields.Selection(get_years(), string='Year')
    maximum_bonus = fields.Many2one('sale.bonuses', string="Maximum Bonus")  # Bono Maximo
    brand_line_objectives_ids = fields.One2many('brand.objectives', "sale_incentive_id",
                                                string="Brand Lines with Objectives")
    state = fields.Selection(
        [('incentive_reg', 'Incentive Registration'),
         ('incentive_sent', 'Incentive Sent'),
         ('incentive_approved', 'Incentive Approved'),
         ('incentive_cancel', 'Incentive Cancelled'),
         ], string='State', default='incentive_reg')

    month_year = fields.Char(string='Month/Year', compute='_compute_month_year', stored=True)

    brands_objective = fields.Integer(string="N° Brands with Objectives")
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
    approved_date = fields.Datetime(string='Approved Date', readonly=True, index=True, help="Date on which the incentive is confirmed.", copy=False)
    
    @api.onchange('supervisor')
    def _is_supervisor(self):
        if self.supervisor:
            self.is_supervisor = True
            self.partner_id = self.supervisor
            
    @api.onchange('seller')
    def _is_seller(self):
        if self.seller:
            self.is_seller = True
            self.partner_id = self.seller

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
        mb = self.maximum_bonus.amount
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
        mb = self.maximum_bonus.amount
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
        mb = self.maximum_bonus.amount
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
                self.bonus_brand_boxes = self.maximum_bonus.amount/self.brands_objective
                

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

    @api.multi
    def action_cancel(self):
        return self.write({'state': 'incentive_sent'})

    @api.multi
    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an incentive in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        self.write({
            'state': 'incentive_approved',
            'approved_date': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
            self.action_done()
        return True

    def _get_forbidden_state_confirm(self):
        return {'incentive_cancel'}
    
    @api.multi
    def print_incentive(self):
        return self.env.ref('sales_modification.incentive_report')\
            .with_context(discard_logo_check=True).report_action(self)

    @api.multi
    def action_incentive_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('sales_modification', 'sale_incentive_email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        lang = self.env.context.get('lang')
        template = template_id and self.env['mail.template'].browse(template_id)
        if template and template.lang:
            lang = template._render_template(template.lang, 'sale.incentive', self.ids[0])
        ctx = {
            'default_model': 'sale.incentive',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'model_description': self.with_context(lang=lang)._description,
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
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_so_as_sent'):
            self.filtered(lambda o: o.state == 'draft').with_context(tracking_disable=True).write({'state': 'incentive_sent'})
            self.env.user.company_id.set_onboarding_step_done('sale_onboarding_sample_quotation_state')
        return super(SaleIncentive, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
           'sale.incentive') or 'New'
        result = super(SaleIncentive, self).create(vals)
        return result

class BrandObjectives(models.Model):
    _name = "brand.objectives"
    _description = "Brand Objectives"

    sale_incentive_id = fields.Many2one('sale.incentive', string='Sale Incentive')
    no_brand_objetive = fields.Char(string="N° Brands with Objectives")
    brand = fields.Many2one('brand.code', string="Brand")  # Marca
    code = fields.Char(string="Code")  # Codigo
    description = fields.Char(string="Description")
    cupor_for_boxes = fields.Float(string="Cupo in boxes")  # Cupor por cajas
    space_in_bs = fields.Float(string="Cupo in Bs")  # Cupo en Bs
    sale_by_box = fields.Float(string="Sale by Boxes")  # Venta por Cajas
    sale_in_bs = fields.Float(string="Sale in Bs")  # Venta en Bs
    achievement_in_box = fields.Float(string="% Achievement in Boxes", compute='_compute_achievement_in_box')  # logro en Cajas
    tobe_charged_for_box = fields.Float(string="To be charged for boxes", compute='_compute_tobe_charged_for_box')  # A cobrar por cajas
    charged_for_box = fields.Float(string="Charge for boxes", compute='_compute_charged_for_box')  # Cobra por cajas


    @api.onchange('brand')
    def onchange_brand(self):
        for rec in self:
            if rec.brand:
                rec.code = rec.brand.code
                rec.no_brand_objetive = str(rec.sale_incentive_id.brands_objective)

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
    _sql_constraints = [
        ('name_uniq',
        'UNIQUE (brand)',
        'Brand name must be unique.')
        ]

    code = fields.Char(string="Code")
    brand = fields.Char(string="Brand")  # Marca


class Region(models.Model):
    _name = "region.incentive"
    _rec_name = 'name'

    code = fields.Char(string="Code")
    name = fields.Char(string="Region")
