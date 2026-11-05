from odoo import fields, models


class FieldPlaygroundA(models.Model):
    _name = "field.playground.a"
    _description = "Playground Parent A: Monetary"

    name = fields.Char(default="Parent A")
    description = fields.Char(string="Description from A")
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    value = fields.Monetary(
        string="Value from A (Monetary)",
        currency_field="currency_id",
        default=10.5,
    )


class FieldPlaygroundB(models.Model):
    _name = "field.playground.b"
    _description = "Playground Parent B: Float"

    name = fields.Char(default="Parent B")
    description = fields.Char(string="Description from B")
    value = fields.Float(string="Value from B (Float)", default=20.5)


class FieldPlaygroundAThenB(models.Model):
    _name = "field.playground.a_then_b"
    _inherit = ["field.playground.a", "field.playground.b"]
    _description = "Playground: A Then B"


class FieldPlaygroundBThenA(models.Model):
    _name = "field.playground.b_then_a"
    _inherit = ["field.playground.b", "field.playground.a"]
    _description = "Playground: B Then A"


class FieldPlaygroundExplicit(models.Model):
    _name = "field.playground.explicit"
    _inherit = ["field.playground.a", "field.playground.b"]
    _description = "Playground: Explicit Float Override"

    value = fields.Float(string="Explicit Float", default=30.5)


class FieldPlaygroundRelated(models.Model):
    _name = "field.playground.related"
    _description = "Playground: Valid Monetary Related Field"

    name = fields.Char(default="Valid related field")
    a_id = fields.Many2one("field.playground.a", required=True)
    currency_id = fields.Many2one(
        "res.currency", related="a_id.currency_id"
    )
    value = fields.Monetary(
        related="a_id.value", currency_field="currency_id"
    )
