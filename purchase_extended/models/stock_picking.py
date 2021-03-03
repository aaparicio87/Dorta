from collections import namedtuple
import json
import time
from datetime import date

from itertools import groupby
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from operator import itemgetter

class stock_picking(models.Model):
    _inherit = "stock.picking"

    def write(self, vals):
        res = super(stock_picking, self).write(vals)
        if self.picking_type_code == 'incoming':
            if vals.get('date_done'):
                for move in self.move_ids_without_package:
                    move.product_id.product_tmpl_id.write_date = vals.get('date_done')

        return res

    # @api.multi
    # def button_validate(self):
    #     print("sleffffffffffffffffffffffff",self)
    #
    #     self.ensure_one()
    #     if not self.move_lines and not self.move_line_ids:
    #         raise UserError(_('Please add some items to move.'))
    #
    #     # If no lots when needed, raise error
    #     picking_type = self.picking_type_id
    #     precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #     no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
    #                              self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
    #     no_reserved_quantities = all(
    #         float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in
    #         self.move_line_ids)
    #     if no_reserved_quantities and no_quantities_done:
    #         raise UserError(_(
    #             'You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))
    #
    #     if picking_type.use_create_lots or picking_type.use_existing_lots:
    #         lines_to_check = self.move_line_ids
    #         if not no_quantities_done:
    #             lines_to_check = lines_to_check.filtered(
    #                 lambda line: float_compare(line.qty_done, 0,
    #                                            precision_rounding=line.product_uom_id.rounding)
    #             )
    #
    #         for line in lines_to_check:
    #             product = line.product_id
    #             if product and product.tracking != 'none':
    #                 if not line.lot_name and not line.lot_id:
    #                     raise UserError(
    #                         _('You need to supply a Lot/Serial number for product %s.') % product.display_name)
    #
    #     if no_quantities_done:
    #         view = self.env.ref('stock.view_immediate_transfer')
    #         wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
    #         return {
    #             'name': _('Immediate Transfer?'),
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'res_model': 'stock.immediate.transfer',
    #             'views': [(view.id, 'form')],
    #             'view_id': view.id,
    #             'target': 'new',
    #             'res_id': wiz.id,
    #             'context': self.env.context,
    #         }
    #
    #     if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
    #         view = self.env.ref('stock.view_overprocessed_transfer')
    #         wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'res_model': 'stock.overprocessed.transfer',
    #             'views': [(view.id, 'form')],
    #             'view_id': view.id,
    #             'target': 'new',
    #             'res_id': wiz.id,
    #             'context': self.env.context,
    #         }
    #
    #     # Check backorder should check for other barcodes
    #     if self._check_backorder():
    #         return self.action_generate_backorder_wizard()
    #     self.action_done()
    #     print("purchase idddddddddddddddddddddddddddddddddddddd", self.action_done())
    #     print ("rec.productttttttttttttt", self.date_done)
    #     return
    #
    # @api.multi
    # def action_done(self):
    #
    #     todo_moves = self.mapped('move_lines').filtered(
    #         lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
    #
    #     for pick in self:
    #         for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
    #             # Search move with this product
    #             moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
    #             moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
    #             if moves:
    #                 ops.move_id = moves[0].id
    #             else:
    #                 new_move = self.env['stock.move'].create({
    #                     'name': _('New Move:') + ops.product_id.display_name,
    #                     'product_id': ops.product_id.id,
    #                     'product_uom_qty': ops.qty_done,
    #                     'product_uom': ops.product_uom_id.id,
    #                     'location_id': pick.location_id.id,
    #                     'location_dest_id': pick.location_dest_id.id,
    #                     'picking_id': pick.id,
    #                     'picking_type_id': pick.picking_type_id.id,
    #                 })
    #                 ops.move_id = new_move.id
    #                 new_move._action_confirm()
    #                 todo_moves |= new_move
    #                 # 'qty_done': ops.qty_done})
    #     todo_moves._action_done()
    #
    #
    #     self.write({'date_done': fields.Datetime.now()})
    #     print("dateeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", self.date_done)
    #     if self.purchase_id:
    #         print("purchase idddddddddddddddddddddddddddddddddddddd",self.purchase_id)
    #         todo_moves = self.mapped('move_lines')
    #         print("moveeeeeeeeeeeeeeeeee lineeeeeeeeeeeeeeeeeeeeeeee", todo_moves)
    #             for rec in todo_moves:
    #             rec.product_id.date_of_last_entry_merchandise = self.date_done
    #             print ("rec.productttttttttttttt",rec.product_id.date_of_last_entry_merchandise)
    #     return True
