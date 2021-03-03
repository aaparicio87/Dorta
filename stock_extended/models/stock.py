from odoo import api, fields, models, _


class stock_picking(models.Model):
    _inherit = "stock.picking"

    order_number = fields.Char("Número de orden")
    user_id = fields.Many2one('res.users',"Responsable")
    document_type = fields.Selection([
        ('reception', 'Recepción'),
        ('transfer', 'Transferir'),
        ('return', 'Regreso'),
        ('delivery', 'Entrega'),
    ], string="Tipo de Documento")
    document = fields.Char("Documento")


    @api.multi
    def open_delivery_guide(self):

        form_id = self.env.ref('stock_extended.view_loading_guides_inherit').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Delivery Guide'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'loading.guides',
            'views': [(form_id, 'form')],
            'context': {
                # 'default_purchase_order_id': self.id,
                'default_partner_id': self.partner_id.id,
            }
        }


class stock_move_line(models.Model):
    _inherit = "stock.move"
    code = fields.Char("Código")
    code_storage = fields.Char("Código de almacenamiento")
    list_pvp = fields.Char("Lista/PVP")
    marked = fields.Char("Marcado")
    u_c = fields.Integer("UxC")
    capp = fields.Float("Capp")
    boxes = fields.Integer("Cajas")
    unit = fields.Integer("Unidades")
    total = fields.Integer("Total")

    @api.onchange('u_c','boxes','product_id')
    def _onchange_total(self):
        self.total = self.u_c * self.boxes
        self.code = self.product_id.default_code