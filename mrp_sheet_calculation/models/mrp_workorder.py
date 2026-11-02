from odoo import api, fields, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'
    
    daily_production_line_ids = fields.One2many(comodel_name="mrp.workorder.daily.production", inverse_name="workorder_id", string="Daily Production Lines")
    qty_in = fields.Float(string="Quantity In")
    qty_in_uom = fields.Many2one(comodel_name="uom.uom",related="workcenter_id.qty_in_uom", string="Quantity In UOM")
    qty_out = fields.Float(string="Quantity Out", compute="_compute_qty_out")
    qty_out_uom = fields.Many2one(comodel_name="uom.uom",related="workcenter_id.qty_out_uom", string="Quantity Out UOM")
    qty_waste = fields.Float(string="Quantity Waste", compute="_compute_qty_waste", store=True)
    waste_percentage = fields.Float(string="Waste Percentage", compute="_compute_waste_percentage", store=True)

    @api.depends('daily_production_line_ids', 'daily_production_line_ids.qty_produced')
    def _compute_qty_out(self):
        for record in self:
            record.qty_out = sum(record.daily_production_line_ids.mapped('qty_produced'))

    @api.depends('qty_in', 'qty_out')
    def _compute_qty_waste(self):
        for record in self:
            record.qty_waste = record.qty_in - record.qty_out / record.qty_in_uom.factor
    
    @api.depends('qty_in', 'qty_waste')
    def _compute_waste_percentage(self):
        for record in self:
            record.waste_percentage = record.qty_waste / record.qty_in if record.qty_in  else 0
