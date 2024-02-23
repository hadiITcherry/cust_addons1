from odoo import models, fields, api


class SallyFlower(models.Model):
    _name = 'sally.flower'
    _description = 'Sally Flowers'
    _rec_name = 'common_name'
    _inherits = {'product.product': 'product_id'}

    product_id = fields.Many2one('product.product', string="Product")

    common_name = fields.Char("Common Name", required=True)
    scientific_name = fields.Char("Scientific Name", required=True)

    season_start_date = fields.Date("Season Start Date")
    season_end_date = fields.Date("Season End Date")

    watering_frequency = fields.Integer("Watering Frequency")
    watering_amount = fields.Float("Watering Amount")

    partner_id = fields.Many2one('res.partner', string='Caretaker', ondelete='restrict', domain=[('name', 'like', 'M%')]
                                 , context={'default_email': 'test@test.com'})
    email = fields.Char(related="partner_id.email")

    partner_ids = fields.Many2many('res.partner', 'partner_flower_relation', 'flower_id', 'partner_id', limit=4)


    def _new_func(self):
        return self


