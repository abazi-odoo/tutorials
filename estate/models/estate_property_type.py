from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence, name"

    sequence = fields.Integer(string="Sequence", default=1)
    name = fields.Char(string="Name", required=True)

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The name of the property type must be unique.'
    )
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            