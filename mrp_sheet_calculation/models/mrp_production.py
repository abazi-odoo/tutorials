from odoo import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    number_of_sheets = fields.Float(string="Number of Sheets", compute="_compute_number_of_sheets", store=True)
    total_sheets_weight = fields.Float(string="Total Sheets Weight", compute="_compute_total_sheets_weight", store=True)
    weight_per_sheet = fields.Float(string="Weight Per Sheet", compute="_compute_weight_per_sheet", store=True)

    @api.depends('product_qty', 'uom_id', 'uom_id.factor', 'product_id.productivity')
    def _compute_number_of_sheets(self):
        for record in self:
            if record.product_id.productivity:
                record.number_of_sheets = record.product_qty * record.uom_id.factor / record.product_id.productivity
            else:
                record.number_of_sheets = 0
            # record.number_of_sheets = record.uom_id._compute_quantity(record.qty_produced, record.uom_id) / record.product_id.productivity

    @api.depends('weight_per_sheet', 'number_of_sheets')
    def _compute_total_sheets_weight(self):
        for record in self:
            record.total_sheets_weight = record.weight_per_sheet * record.number_of_sheets

    @api.depends('product_id.sheet_length', 'product_id.sheet_width', 'product_id.gsm')
    def _compute_weight_per_sheet(self):
        for record in self:
            if record.product_id.sheet_length and record.product_id.sheet_width and record.product_id.gsm:
                record.weight_per_sheet = (record.product_id.sheet_length / 100.0) * (record.product_id.sheet_width / 100.0 ) * (record.product_id.gsm/ 1000.0)
            else:
                record.weight_per_sheet = 0.0
