# -*- coding : utf-8 -*-

from odoo import models, fields


class FoodItems(models.Model):
    _name = 'room.food'
    _description = 'Food products'
    _rec_name = 'food_name'

    food_name = fields.Char(string="Name")
    category_id = fields.Many2one('food.category')
    image = fields.Image()
    price = fields.Float()


class FoodCategory(models.Model):
    _name = 'food.category'
    _description = 'Food category'
    _rec_name = 'category_name'

    category_name = fields.Char(string="Category", required="True")
