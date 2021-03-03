# -*- coding: utf-8 -*-
from datetime import date, datetime

from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo import api, fields, models


class ShoppingPrograms(models.Model):
    _name = "shopping.program"
    _rec_name = 'responsible_id'

    shopping_year = fields.Char(string="Ano")
    order_date = fields.Date(string="Fecha de Solicitud de Orden")
    responsible_id = fields.Many2one('res.users', string="Responsable")
    state = fields.Selection([('borrador', 'Borrador'),
                              ('abierto', 'Abierto'),
                              ('Cerradoo', 'Cerradoo'),
                              ('cerrado', 'Cerrado')], string="Estado", default='borrador')
    shopping_config_ids = fields.One2many('shopping.program.config', 'shopping_program_id')
    order_boolean = fields.Boolean(string="Booleano de la orden")
    january = fields.Boolean(string="Enero")
    february = fields.Boolean(string="Febrero")
    march = fields.Boolean(string="Marzo")
    april = fields.Boolean(string="Abril")
    may = fields.Boolean(string="Mayo")
    june = fields.Boolean(string="Junio")
    july = fields.Boolean(string="Julio")
    august = fields.Boolean(string="Agosto")
    september = fields.Boolean(string="Septiembre")
    october = fields.Boolean(string="Octubre")
    november = fields.Boolean(string="Noviembre")
    december = fields.Boolean(string="Diciembre")

    @api.multi
    def shopping_program_scheduler(self):
        res = self.env['shopping.program'].search([])
        for rec in res:
            if date.today().strftime('%Y') == rec.shopping_year:
                for shopping_program in rec.shopping_config_ids:
                    purchase_order = self.env['purchase.order'].search([('id', '=', shopping_program.reference_id.id)])
                    product_id = shopping_program.product_id
                    if date.today().strftime('%B') == 'January' or rec.january:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.january,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price
                                })
                    if date.today().strftime('%B') == 'February' or rec.february:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.february,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'March' or rec.march:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.march,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'April' or rec.april:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.april,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if date.today().strftime('%B') == 'May' or rec.may:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.may,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if date.today().strftime('%B') == 'June' or rec.june:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.june,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'July' or rec.july:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.july,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'August' or rec.august:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.august,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'September' or rec.september:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.september,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'October' or rec.october:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.october,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'November' or rec.november:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.november,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })
                    if date.today().strftime('%B') == 'December' or rec.december:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                    'order_id': purchase_order.id,
                                    'product_id': product_id.id,
                                    'name': product_id.name,
                                    'product_qty': shopping_program.december,
                                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                    'price_unit': product_id.standard_price,  # product_id.price_unit
                                })

    @api.multi
    def shopping_program_create(self):
        for rec in self.env['shopping.program'].browse(self._context.get('active_id')):
            rec.january = self.january
            rec.february = self.february
            rec.march = self.march
            rec.april = self.april
            rec.may = self.may
            rec.june = self.june
            rec.july = self.july
            rec.august = self.august
            rec.september = self.september
            rec.october = self.october
            rec.november = self.november
            rec.december = self.december
            if date.today().strftime('%Y') == rec.shopping_year:
                for shopping_program in rec.shopping_config_ids:
                    purchase_order = self.env['purchase.order'].search([('id', '=', shopping_program.reference_id.id)])
                    product_id = shopping_program.product_id
                    if rec.january:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.january,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price
                            })
                    if rec.february:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.february,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.march:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.march,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.april:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.april,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.may:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.may,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.june:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.june,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.july:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.july,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.august:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.august,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.september:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.september,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.october:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.october,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.november:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.november,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })
                    if rec.december:
                        if product_id:
                            self.env['purchase.order.line'].create({
                                'order_id': purchase_order.id,
                                'product_id': product_id.id,
                                'name': product_id.name,
                                'product_qty': shopping_program.december,
                                'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                'product_uom': product_id.uom_po_id.id or product_id.uom_id.id,
                                'price_unit': product_id.standard_price,  # product_id.price_unit
                            })

    def confirm_scheduled_purchase(self):
        for order in self:
            order.state = 'abierto'


    def cancel_shopping_program(self):
        for order in self:
            order.state = 'cerrado'

    @api.multi
    def send_mail_shopping(self):

        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('purchase_extended', 'email_template_shopping_program')[1]
        except ValueError:
            template_id = False
        ctx = {
            'default_model': 'shopping.program',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'email_from': self.env.user.email,
            'force_send': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            # 'views': [(compose_form_id, 'form')],
            # 'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class ShoppingProgramsconfig(models.Model):
    _name = "shopping.program.config"

    reference_id = fields.Many2one('purchase.order', string="Purchase Order")
    reference = fields.Char(string="Reference")
    product_id = fields.Many2one('product.product', string="Product")
    shopping_program_id = fields.Many2one('shopping.program', string="Shopping Program")
    january = fields.Float(string="January")
    february = fields.Float(string="February")
    march = fields.Float(string="March")
    april = fields.Float(string="April")
    may = fields.Float(string="May")
    june = fields.Float(string="June")
    july = fields.Float(string="July")
    august = fields.Float(string="August")
    september = fields.Float(string="September")
    october = fields.Float(string="October")
    november = fields.Float(string="November")
    december = fields.Float(string="December")
