# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    alcohol_grade = fields.Float(string="Grado de Alcohol")
    pro_cat_type = fields.Boolean(related="categ_id.alcoholic", string="Tipo de Categoría de Productos")


class ProductCategoryExtend(models.Model):
    _inherit = "product.category"

    alcoholic = fields.Boolean(string="Categoría Alcohólica",
                               help="Si esta categoría se utilizará para productos alcohólicos, entonces debe marcada")
