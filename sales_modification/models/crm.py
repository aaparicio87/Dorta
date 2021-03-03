# -*- coding: utf-8 -*-

from odoo import models, fields, api

SEPARATOR = ' / '


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    hierarchical_level_id = fields.Many2one('crm.team', string="Hierarchical Level")
    image_medium = fields.Binary(string="Image")
    email = fields.Char(string="Email Address")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    cargo = fields.Selection([('manager', 'Manager'),
                              ('analyst', 'Analyst')], string='Cargo')

    # def name_get(self):
    #     full_name = ''
    #     if self.hierarchical_level_id:
    #         full_name += self.get_parent_name()
    #     else:
    #         return self.name
    #
    # def get_parent_name(self):
    #     return self.hierarchical_level_id.name