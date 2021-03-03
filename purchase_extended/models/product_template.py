from odoo import api, fields, models


class product_template(models.Model):
    _inherit = "product.template"

    product_nationality = fields.Selection([('national', 'National'), ('imported', 'Imported')], default='national',
                                           string='Product Nationality')
    # date_of_last_entry_merchandise = fields.Datetime("Date of last entry of merchandise")
    # custom_purchase_id = fields.Many2one('custom.purchase')
    partial_tax_id = fields.Many2one('account.tax', string="Partial Taxes")
    perception_iva = fields.Float(string="Perception IVA", compute="set_product_iva")
    unit_measure_id = fields.Many2one('uom.uom', string="Unite Of Measure")
    purchase_unit_measure_id = fields.Many2one('uom.uom', string="Purchase Unite Of Measure")

    # @api.onchange('product_nationality', 'partial_tax_id')
    # def _onchange_calculation(self):
    #     if self.product_nationality == 'imported':
    #         total = self.list_price * self.standard_price * self.partial_tax_id / 100
    #         iva_amount = self.standard_price * self.partial_tax_id / 100
    #         perception_iva = total - iva_amount
    #         self.perception_iva = perception_iva

    @api.depends('product_nationality')
    def set_product_iva(self):
        for rec in self:
            if rec.product_nationality == 'imported':
                custom_purchase_ids = self.env['custom.purchase'].search([], order='create_date desc')
                if custom_purchase_ids:
                    rec.perception_iva = custom_purchase_ids[0].pereception_vat_bs


