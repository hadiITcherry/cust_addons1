
from odoo import models, fields, api


class quico(models.Model):
    _name = 'quico.quico'
    _description = 'quico.quico'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

# class QuicoSaleOrder(models.Model):
#     _name = "quico.sale.order"
#     _inherit = "sale.order"
