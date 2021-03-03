from odoo import api, fields, models, _
from datetime import datetime


class custom_purchase(models.Model):
    _name = "custom.purchase"
    _rec_name = "code"
    _order = 'id desc'

    code = fields.Char("Codigo")
    barcode = fields.Char("Codigo de Barras")
    note = fields.Char("Nota")
    box_barcode = fields.Char("Codigo de Barras de la caja")
    category_id = fields.Many2one('product.category',"Categoria")
    product_id = fields.Many2one('product.template',"Nombre del Producto")
    gl = fields.Char("GL")
    cap = fields.Char("Cap")
    u_c = fields.Char("U/C")
    origin = fields.Char("Origen")
    price_list = fields.Selection("Lista de Precios")
    price_list = fields.Selection([
        ('firm_ground', 'Firm Ground'),
        ('free_port', 'Free Port'),
    ], string='Lista de Precios',)
    applies_date = fields.Date("Fecha de Aplicacion")

    bs_petro = fields.Float("BS x PETRO ")
    bs_us_op_week = fields.Float("BS x UC $ Apertura de la semana ")
    increase_per = fields.Float("Porcentaje de Incremento")
    total = fields.Float("Total")
    trade_margin_sugested_price = fields.Float("Comercio de % de Margen para precio sugerido")
    in_change_list_price = fields.Float(compute='increase_change_listing',string="Incremento de Cambio de Bs. Para Escucha de Precios Online")
    total_price_list_bs = fields.Float(compute='increase_change_listing',string="Precio Total Unico De la Lista Bs")
    pvp_imp_boxbs = fields.Float(compute='increase_change_listing', string="PVP+IMP x Caja Bs")
    q5_per = fields.Float("16%")
    tax_rrp_bs = fields.Float("Impuestos RRP Bs")
    box_pvp_boxbs = fields.Float(compute='increase_change_listing', string="Base PVP x Box Bs")
    base_pvp_bsunit = fields.Float(compute='increase_change_listing', string="PVP + IMP x Bs Unidad")
    pvp_imp_box = fields.Float(compute='increase_change_listing', string="PVP + IMP x Caja")
    pvp_imp_unit = fields.Float(compute='increase_change_listing', string="PVP + IMP x Unidad")
    value_marchandise_bs = fields.Float(compute='increase_change_listing', string="Valor de la mercancia Bs")
    iva_bs = fields.Float(compute='increase_change_listing', string="IVA Bs")
    pereception_vat_bs = fields.Float(compute='increase_change_listing', store=True, string="Percepcion de IVA en Bs")
    total_transfer_national_tax = fields.Float(compute='increase_change_listing', string="Impuestos totales en transferencias nacionales Bs")
    precio_total_caja_bs = fields.Float(compute='increase_change_listing', string="Precio Total x Caja Bs")
    total_price_unit_bs = fields.Float(compute='increase_change_listing', string="Precio Total x Unidad Bs")


    def increase_change_listing(self):
        for rec in self:
            rec.in_change_list_price = rec.bs_us_op_week * rec.increase_per / 100 + rec.bs_us_op_week
            rec.total_price_list_bs = rec.total * rec.in_change_list_price
            trade_margin = 1 - rec.trade_margin_sugested_price / 100
            rec.pvp_imp_boxbs = rec.total_price_list_bs / trade_margin
            if rec.pvp_imp_boxbs and (rec.u_c):
                rec.base_pvp_bsunit = rec.pvp_imp_boxbs / float(rec.u_c)
            if rec.pvp_imp_boxbs and rec.bs_petro:
                rec.pvp_imp_box = rec.pvp_imp_boxbs / rec.bs_petro
            if rec.pvp_imp_box and (rec.u_c):
                rec.pvp_imp_unit = rec.pvp_imp_box / float(rec.u_c)
            q5_per = 1 + rec.q5_per / 100
            total_pvp = rec.pvp_imp_boxbs - rec.tax_rrp_bs
            rec.box_pvp_boxbs = total_pvp / q5_per
            m7_p7_value_marchandise_bs = rec.total_price_list_bs - rec.tax_rrp_bs
            v7_q5_value_marchandise_bs = rec.box_pvp_boxbs * rec.q5_per / 100
            rec.value_marchandise_bs = m7_p7_value_marchandise_bs - v7_q5_value_marchandise_bs
            rec.iva_bs = rec.value_marchandise_bs * rec.q5_per / 100
            rec.pereception_vat_bs = (rec.box_pvp_boxbs * rec.q5_per / 100) - rec.iva_bs
            rec.total_transfer_national_tax = rec.tax_rrp_bs + rec.iva_bs + rec.pereception_vat_bs
            rec.precio_total_caja_bs = rec.value_marchandise_bs + rec.total_transfer_national_tax
            if rec.precio_total_caja_bs and (rec.u_c):
                rec.total_price_unit_bs = rec.precio_total_caja_bs / float(rec.u_c)
    @api.onchange('product_id')
    def set_product(self):
        for rec in self:
            if rec.product_id:
                rec.category_id = rec.product_id.categ_id
                rec.barcode = rec.product_id.barcode
