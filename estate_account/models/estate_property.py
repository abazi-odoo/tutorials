from odoo import models, Command

class InheritedModel(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        account_move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            # 'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
            'invoice_line_ids': [
                Command.create({
                'name': self.name + ' Selling Price',
                'quantity': 1,
                'price_unit': self.selling_price,
            }),
                Command.create({
                'name': self.name + ' Commission',
                'quantity': 1,
                'price_unit': 0.06 * self.selling_price,
            }),
                Command.create({
                'name': self.name + ' Administrative Fees',
                'quantity': 1,
                'price_unit': 100,
            })],
        })
        return super().action_sold()