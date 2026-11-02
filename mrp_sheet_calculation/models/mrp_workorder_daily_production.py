from odoo import fields, models


class MrpWorkorderDailyProduction(models.Model):
    _name = 'mrp.workorder.daily.production'
    
    date = fields.Date()
    notes = fields.Char()
    qty_produced = fields.Float()
    
    responsible_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Responsible"
    )
    
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="UOM")
    
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder",
        string="Work Order"
    )
