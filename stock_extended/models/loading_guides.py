from odoo import api, fields, models, _
from datetime import date

class loading_guides(models.Model):
    _name = "loading.guides"
    _rec_name ="partner_id"

    states = fields.Selection(
        [('eraser', 'Borrador'),
         ('on_hold', 'En espera'),
         ('prepared', 'Preparado'),
         ('done', 'Hecho'),
         ], string='Status', default='eraser')

    user_id = fields.Many2one('res.users',string="Creado por")
    guide = fields.Char("Nro Guía")
    driver = fields.Char("Conductor")
    transport_plate = fields.Char("Placa de transporte")
    create_date = fields.Date("Fecha de creación")
    company_id = fields.Many2one('res.company')
    partner_id = fields.Many2one('res.partner',string="Elaborado por")
    related_invoice_id = fields.Many2one('account.invoice',string="Factura relacionada")
    board = fields.Char("Tablero")
    model = fields.Char("Modelo")
    delivery_order_id = fields.Many2one('stock.picking',"Orden de entrega")
    capacity = fields.Char("Capacidad")
    brand = fields.Char("Marca")
    route = fields.Char("Ruta")
    # conductor = fields.Char("Conductor")
    assistance = fields.Char("Asistencia")
    zone_dispatch = fields.Char("Zona para despachar")
    product_list_id = fields.One2many("product.list","product_list_line", string="Lista de productos")

    def action_done(self):
        for rec in self:
            rec.states = 'done'

    def action_eraser(self):
       for rec in self:
            rec.states = 'eraser'

    def action_prepared(self):
        for rec in self:
            rec.states = 'prepared'

    def action_on_hold(self):
        for rec in self:
            rec.states = 'on_hold'


    @api.onchange('delivery_order_id')
    def onchange_product_list(self):
        update_line =[]
        for line in self.delivery_order_id.move_ids_without_package:
            print("lineeeeeeeeeeeeeeeeeeee",line.capp)
            update_line.append((0,0,{'discription':line.product_id.name,
                                     'code':line.product_id.default_code,
                                     'cap':line.capp,
                                     'uxc':line.u_c,
                                     'box':line.boxes,
                                     'total_kgs':line.total,
                                     }))
        self.product_list_id = update_line


class product_list(models.Model):
    _name = "product.list"

    product_list_line = fields.Many2one("loading.guides")
    code = fields.Char("Code")
    discription = fields.Char("Descripción/Producto")
    cap = fields.Char("Cap")
    uxc = fields.Char("U*C")
    box = fields.Char("Cajas")
    unds = fields.Char("Unds")
    kgs_prod = fields.Char("Kgs * Prod")
    total_kgs = fields.Char("Total Kgs")
    cpi = fields.Char("CPI")

