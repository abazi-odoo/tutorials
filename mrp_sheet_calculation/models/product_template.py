from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    gsm = fields.Float(string= "GSM (g/m²)")
    productivity = fields.Float()
    sheet_length = fields.Float(string="Sheet Length (cm)")
    sheet_width = fields.Float(string="Sheet Width (cm)")
