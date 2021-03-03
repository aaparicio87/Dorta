# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    note_for_invoice = fields.Text(string="Nota para Factura")
    terms_conditions = fields.Selection([('days_of_delivery_of_notifications', 'Días de entrega de notificaciones'),
                                         ('notice', 'Aviso'),
                                         ('delivery_day', 'Días de entrega de mercancía')],
                                        string="Términos y Condiciones ")