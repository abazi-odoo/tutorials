from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=lambda self: fields.Date.context_today(self) + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
            ],
            default='new',
            required=True,
            copy=False,
        )
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
    )
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be greater than 0.',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be greater than or equal to 0.',
    )
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = False
            if record.garden and record.garden_area == 0:
                record.garden_area = 10
                record.garden_orientation = 'north'
    
    def action_sold(self):
        for record in self:
            if record.state == 'offer_accepted':
                record.state = 'sold'
            else:
                raise UserError("Only properties with accepted offers can be marked as sold.")
    
    def action_cancel(self):
        for record in self:
            if record.state in ['new', 'offer_received', 'offer_accepted']:
                record.state = 'cancelled'
            else:
                raise UserError("Only properties that are new, have received offers, or have accepted offers can be cancelled.")

    @api.constrains('selling_price', 'expected_price')
    def _check_offer_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            elif float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("Offer price must be at least 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_or_cancelled(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise ValidationError("You can only delete properties that are new or cancelled.")
