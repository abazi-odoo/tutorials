from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        readonly=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be greater than 0.',
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            for subrecord in record.property_id.offer_ids:
                if record.id != subrecord.id:
                    subrecord.status = "refused"

    def action_refuse(self):
        for record in self:
            if record.status != "refused":
                record.property_id.selling_price = 0.0
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env["estate.property"].browse(vals["property_id"])
            price = vals["price"]

            if price <= max(property_record.offer_ids.mapped("price"), default=0):
                raise ValidationError(_("Offer price must be greater than the current highest offer."))
            else:
                property_record.state = "offer_received"
        return super().create(vals_list)