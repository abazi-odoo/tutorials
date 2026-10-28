from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
    
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The name of the property tag must be unique.'
    )