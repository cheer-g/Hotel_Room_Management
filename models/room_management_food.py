# -*- coding : utf-8 -*-

from odoo import models, fields, api


class FoodItems(models.Model):
    _name = 'room.food'
    _description = 'Food products'
    _rec_name = 'food_name'

    def _compute_subtotal_price(self):
        """
        Compute total price based on the quantity ordered
        """
        # print("Acco :", self.accommodation_entry)
        for rec in self:
            rec.subtotal_price = rec.price_sale * rec.quantity

    def _compute_accommodation_id(self):
        for rec in self:
            if rec.order_id:
                self.update({'accommodation_id': rec.order_id.accommodation_id})
            else:
                self.update({'accommodation_id': False})
            print("Acco : ", rec.accommodation_id)

    food_name = fields.Char(string="Name")
    category_id = fields.Many2one('food.category')
    image = fields.Image()
    price = fields.Float()

    order_id = fields.Many2one('order.food')
    accommodation_id = fields.Many2one('room.accommodation',
                                       default=_compute_accommodation_id,
                                       string="Accommodation ID", store="True")
    quantity = fields.Integer(string="Quantity", default='1')
    description = fields.Text(string="Description")
    image_view = fields.Image(related='food_id.image')
    food_id = fields.Many2one('room.food')
    price_sale = fields.Float(related='food_id.price')
    subtotal_price = fields.Float(compute=_compute_subtotal_price,
                                  string="Subtotal")
    amount_total = fields.Float()
    category_id_view = fields.Char()

    @api.onchange('food_id')
    def _onchange_food_id(self):
        self.update({'description': self.food_id.description})


class FoodCategory(models.Model):
    _name = 'food.category'
    _description = 'Food category'
    _rec_name = 'category_name'

    category_name = fields.Char(string="Category", required="True")
