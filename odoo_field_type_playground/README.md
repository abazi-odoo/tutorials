# Field Type Inheritance Playground (Odoo 20)

An isolated, installable module for testing Odoo's resolution of duplicate
field names in classical multiple inheritance (`_inherit`) and comparing that
with the strict field-type check for related fields.

## Included cases

| Model | Definition | Expected `value` type |
| --- | --- | --- |
| `field.playground.a` | `fields.Monetary` | `monetary` |
| `field.playground.b` | `fields.Float` | `float` |
| `field.playground.a_then_b` | `_inherit = ["field.playground.a", "field.playground.b"]` | `monetary` |
| `field.playground.b_then_a` | `_inherit = ["field.playground.b", "field.playground.a"]` | `float` |
| `field.playground.explicit` | Inherits A, B; explicitly declares Float | `float` |
| `field.playground.related` | Correct Monetary related field | `monetary` |

The parent models also declare `description = fields.Char(...)` with different
labels, for inspecting conflicts between fields of the **same** type.

## Install

1. Unzip. Put the **entire `odoo_field_type_playground` folder** inside an
   addons directory included in your `--addons-path` (e.g. `tutorials/`).
2. Use a **throwaway database**, not a production or important development DB.
3. Restart Odoo, update the Apps list if necessary, and install
   **Field Type Inheritance Playground**.
4. Open the **Field Type Playground** app to create records in the three
   combined models. Change the inheritance order in `models/field_cases.py`,
   restart, and upgrade the module to experiment further.

## Inspect the actual resolved definitions in Odoo shell

From your Odoo source directory, run (adjust paths and database name):

```bash
./odoo-bin shell -d YOUR_TEST_DB --addons-path="addons,../enterprise,../tutorials"
```

Then paste:

```python
for model_name in (
    "field.playground.a",
    "field.playground.b",
    "field.playground.a_then_b",
    "field.playground.b_then_a",
    "field.playground.explicit",
    "field.playground.related",
):
    value = env[model_name]._fields["value"]
    print(f"{model_name}: type={value.type}, class={type(value).__name__}, label={value.string}")
```

To inspect a same-type name collision:

```python
for model_name in ("field.playground.a_then_b", "field.playground.b_then_a"):
    field = env[model_name]._fields["description"]
    print(model_name, field.type, field.string)
```

## Reproduce the Monetary/Float *related-field* error

This scenario is **disabled by default** because it intentionally prevents
the registry from loading:

1. Open `models/__init__.py`.
2. Uncomment `from . import broken_related`.
3. Restart Odoo and upgrade the module **only on a disposable database**.
4. Odoo should raise a related-field type inconsistency during model setup.
   `field.playground.broken_related.value` is `Float`, but its target
   `field.playground.a.value` is `Monetary`.
5. Comment out the import again and restart to restore the working code.

This illustrates why a fresh multiple-inheritance field-name collision can be
resolved while an explicitly declared *related* field of the wrong type fails.

## Run automated tests (optional)

Install the module with tests enabled in a disposable database:

```bash
./odoo-bin -d YOUR_TEST_DB --addons-path="addons,../enterprise,../tutorials" \
    -i odoo_field_type_playground --test-enable --stop-after-init
```

No external dependencies beyond standard Odoo `base` are required.
