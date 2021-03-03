# -*- coding: utf-8 -*-

from odoo import models, fields, api

SEPARATOR = ' / '


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    hierarchical_level_id = fields.Many2one('crm.team.hierarchical', string="Hierarchical Level")
    
class CrmTeamHierarchical(models.Model):

    _name = 'crm.team.hierarchical'
    _description = 'Hierarchical Level'

    name = fields.Char(string="Name")
    image_medium = fields.Binary(string="Image")
    email = fields.Char(string="Email Address")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    cargo = fields.Selection([('manager', 'Manager'),
                              ('analyst', 'Analyst')], string='Cargo')
    company_id = fields.Many2one('res.company', string='Company')