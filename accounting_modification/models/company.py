# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    nit = fields.Char(string="NIT")
    license = fields.Char(string="Licencia")
