# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerModify(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one(string="Seller")
    seller_code = fields.Integer(string="Seller Code")
    payment_deadline = fields.Integer(string="Payment deadline",
                                      help="Periods in days, to send email to Salesperson for reminder of pending "
                                           "invoices.")
    deadline_last_send = fields.Date(string="Last email send Date")
    license = fields.Char(string="License")
    responsible = fields.Char(string="Responsible")
    business_name = fields.Char(string="Business name")
    trade_name = fields.Char(string="Trade Name")
    litration = fields.Char(string="Litration")
    channel_id = fields.Many2one('res.partner.channel', string="Channel", ondelete='restrict')
    sub_chanel_id = fields.Many2one('res.partner.subchannel', string="SubChannel", domain="[('channel_id', '=?', channel_id)]")


class Channel(models.Model):
    _name = "res.partner.channel"

    name = fields.Char(string="Channel")
    sub_channel_ids = fields.One2many('res.partner.subchannel', 'channel_id', string='Subchannel')

class SubChannel(models.Model):
    _name = "res.partner.subchannel"

    name = fields.Char(string="Subchannel")
    channel_id = fields.Many2one('res.partner.channel', string='Channel')