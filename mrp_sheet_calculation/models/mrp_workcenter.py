from odoo import fields, models


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    qty_in_uom = fields.Many2one(comodel_name="uom.uom", string="Quantity in UOM")
    qty_out_uom = fields.Many2one(comodel_name="uom.uom", string="Quantity out UOM")
