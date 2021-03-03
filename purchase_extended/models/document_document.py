from odoo import api, models, fields, _
import PyPDF2 as pyPdf


class document_document(models.Model):
    _name = 'document.document'

    name = fields.Char("Name")
    type_id = fields.Many2one('type.type',"Type")
    document = fields.Binary('Upload Your File', attachment=True)

class type_type(models.Model):
    _name = 'type.type'

    name = fields.Char("Name")