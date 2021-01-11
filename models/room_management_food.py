# -*- coding : utf-8 -*-

from odoo import models, fields, api


class FoodItems(models.Model):
    _name = 'room.food'
    _description = 'Food products'
    _rec_name = 'food_name'

    food_name = fields.Char(string="Name")
    category_id = fields.Many2one('food.category')
    image = fields.Image()
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True)
    price = fields.Float()
    description = fields.Text()


class FoodCategory(models.Model):
    _name = 'food.category'
    _description = 'Food category'
    _rec_name = 'category_name'

    category_name = fields.Char(string="Category", required="True")
