# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PosDetails(models.TransientModel):
    _name = 'liquor.book.report.wizard'
    _description = 'Asistente para Informes del Libro de Licores'

    start_date = fields.Date(string="Fecha Inicio")
    end_date = fields.Date(string="Fecha Fin")

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def generate_report(self):
        in_stock_moves = self.env['stock.move'].search(
            [("date", ">=", self.start_date), ("date", "<=", self.end_date),
             ('state', 'not in', ('cancel', 'assigned')),
             ('location_id.usage', 'not in', ('internal', 'transit')),
             ('location_dest_id.usage', 'in', ('internal', 'transit')), ('product_id.pro_cat_type', '=', True),
             ('picking_type_id', '!=', False)])
        out_stock_moves = self.env['stock.move'].search(
            [("date", ">=", self.start_date), ("date", "<=", self.end_date),
             ('state', 'not in', ('cancel', 'assigned')),
             ('location_id.usage', 'in', ('internal', 'transit')),
             ('location_dest_id.usage', 'not in', ('internal', 'transit')),
             ('product_id.pro_cat_type', '=', True),
             ('picking_type_id', '!=', False)])
        if len(in_stock_moves) <= 0 or len(out_stock_moves) <= 0:
            raise ValidationError(_('Datos no encontrados. Seleccione las fechas válidas.'))
        else:
            return self.env.ref('accounting_modification.liquor_book_report_action').report_action([], data={
                'date_start': self.start_date, 'date_stop': self.end_date})

    def get_in_liquor_book_report(self, date_start, date_end):
        """ ("IN")
        Get stock.move which are in "Receipts" and which products's category is Alcoholic type.
        :param date_start: Start date which select in wizard.
        :param date_end: End date which select in wizard.
        :return: Record of Receipts between start date and end date.
        """
        in_stock_moves = self.env['stock.move'].search(
            [("date", ">=", date_start), ("date", "<=", date_end), ('state', 'not in', ('cancel', 'assigned')),
             ('location_id.usage', 'not in', ('internal', 'transit')),
             ('location_dest_id.usage', 'in', ('internal', 'transit')),
             ('product_id.pro_cat_type', '=', True),
             ('picking_type_id', '!=', False)])
        return in_stock_moves

    def get_out_liquor_book_report(self, date_start, date_end):
        """ ("OUT")
        Get stock.move which are in "Delivery Orders" and which products's category is Alcoholic type.
        :param date_start: Start date which select in wizard.
        :param date_end: End date which select in wizard.
        :return: Record of Delivery Orders between start date and end date.
        """
        out_stock_moves = self.env['stock.move'].search(
            [("date", ">=", date_start), ("date", "<=", date_end), ('state', 'not in', ('cancel', 'assigned')),
             ('location_id.usage', 'in', ('internal', 'transit')),
             ('location_dest_id.usage', 'not in', ('internal', 'transit')),
             ('product_id.pro_cat_type', '=', True),
             ('picking_type_id', '!=', False)])
        return out_stock_moves

    def get_total_entries(self, date_start, date_end):
        """ (IN)
        Get total done quantities from stock.move which are in "Receipts" and which products's category is Alcoholic type.
        :param date_start: Start date which select in wizard.
        :param date_end: End date which select in wizard.
        :return: Total In quantities (Total Entries)
        """
        total_in = 0.0
        in_stock_moves = self.env['stock.move'].search(
            [("date", ">=", date_start), ("date", "<=", date_end), ('state', 'not in', ('cancel', 'assigned')),
             ('location_id.usage', 'not in', ('internal', 'transit')),
             ('location_dest_id.usage', 'in', ('internal', 'transit')), ('product_id.pro_cat_type', '=', True),
             ('picking_type_id', '!=', False)])
        total_in = sum(qty.quantity_done for qty in in_stock_moves)
        return total_in

    def get_total_departures(self, date_start, date_end):
        """ (OUT)
        Get total done quantities from stock.move which are in "Delivery Orders" and which products's category is Alcoholic type.
        :param date_start: Start date which select in wizard.
        :param date_end: End date which select in wizard.
        :return: Total Out quantities (Total Departures)
        """
        total_out = 0.0
        out_stock_moves = self.env['stock.move'].search(
            [("date", ">=", date_start), ("date", "<=", date_end), ('state', 'not in', ('cancel', 'assigned')),
             ('location_id.usage', 'in', ('internal', 'transit')),
             ('location_dest_id.usage', 'not in', ('internal', 'transit')),
             ('product_id.pro_cat_type', '=', True),
             ('picking_type_id', '!=', False)])
        total_out = sum(qty.quantity_done for qty in out_stock_moves)
        return total_out
