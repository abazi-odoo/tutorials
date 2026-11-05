import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestInheritedFieldTypes(TransactionCase):
    def test_type_resolution_by_parent_order(self):
        cases = {
            "field.playground.a_then_b": "monetary",
            "field.playground.b_then_a": "float",
            "field.playground.explicit": "float",
        }
        for model_name, expected_type in cases.items():
            with self.subTest(model=model_name):
                field = self.env[model_name]._fields["value"]
                _logger.info(
                    "%s.value: type=%s, field_class=%s, label=%s",
                    model_name,
                    field.type,
                    type(field).__name__,
                    field.string,
                )
                self.assertEqual(field.type, expected_type)

    def test_compatible_related_field(self):
        field = self.env["field.playground.related"]._fields["value"]
        self.assertEqual(field.type, "monetary")
