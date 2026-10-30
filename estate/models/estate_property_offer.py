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
        self.date_deadline = (self.create_date.date() + relativedelta(days=self.validity))

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.status = "accepted"

        for record in self:
            record.property_id.update({
                'state':"offer_accepted",
                'buyer_id':record.partner_id,
                'selling_price': record.price    
            })
        
        declined_offers = self.property_id.offer_ids - self
        declined_offers.status = "refused"

    def action_refuse(self):
        self.filtered(lambda o :o.status == "accepted").property_id.selling_price = 0
        self.status = "refused"
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0.0
            record.status = "refused"
        self.update({
            
            "status": "refused"
        })
        

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env["estate.property"].browse(vals["property_id"])
            if vals["price"] <= max(property_record.offer_ids.mapped("price"), default=0):
                raise ValidationError(_("Offer price must be greater than the current highest offer."))
            else:
                property_record.state = "offer_received"
        return super().create(vals_list)
