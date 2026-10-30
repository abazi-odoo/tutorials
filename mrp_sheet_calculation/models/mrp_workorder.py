from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    #daily_production_line_ids = fields.One2many(comodel_name="mrp_workorder_daily_production", inverse_field="workorder_id", string="Daily Production Lines")
    qty_in = fields.Float(String="Quantity In")
    qty_in_uom = fields.Many2one(comodel_name="uom.uom",related="workcenter_id.qty_in_uom", string="Quantity In UOM")
    qty_out = fields.Float(String="Quantity Out", compute="_compute_qty_out")
    qty_out_uom = fields.Many2one(comodel_name="uom.uom",related="workcenter_id.qty_out_uom", string="Quantity Out UOM")
    qty_waste = fields.Float(string="Quantity Waste", compute="_compute_qty_waste", store=True)
    waste_percentage = fields.Float(string="Waste Percentage", compute="_compute_waste_percentage", store=True)

    def _compute_qty_out(self):
        for record in self:
            record.qty_out = sum(record.daily_production_line_ids.mapped('quantity_producted'))

    def _compute_qty_waste(self):
        for record in self:
            record.qrt_waste = record.qty_in - record.qty_out
    
    def _compute_waste_percentage(self):
        for record in self:
            if record.qrt_in:
                record.waste_percentage = record.qty_waste / record.qty_in
            else:
                record.waste_percentage = 0.0