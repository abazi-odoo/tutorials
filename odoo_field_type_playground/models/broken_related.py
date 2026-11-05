"""INTENTIONALLY BROKEN example. Do not import in normal installations.

To reproduce a related-field type mismatch, uncomment its import in
models/__init__.py, then restart Odoo and upgrade the module on a throwaway DB.
The target a_id.value is Monetary, while this related value is Float.
"""

from odoo import fields, models


class FieldPlaygroundBrokenRelated(models.Model):
    _name = "field.playground.broken_related"
    _description = "Playground: Intentionally Broken Related Field"

    a_id = fields.Many2one("field.playground.a")
    value = fields.Float(related="a_id.value")
