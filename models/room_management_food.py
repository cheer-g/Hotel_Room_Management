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
        for rec in self:
            rec.subtotal_price = rec.price * rec.quantity

    def _compute_price(self):
        """Compute item price"""
        for rec in self:
            if not rec.rent:
                rec.update({'price_view': rec.food_id.price})
            else:
                rec.price_view = 0

    food_name = fields.Char(string="Name")
    category_id = fields.Many2one('food.category')
    image = fields.Image()
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True)
    price = fields.Float()
    description = fields.Text()

    order_id = fields.Many2one('order.food')
    # accommodation_id = fields.Many2one('room.accommodation',
    #                                    related='order_id.accommodation_id',
    #                                    string="Accommodation ID")
    orders_id = fields.Char()
    accommodation_id = fields.Char(related='order_id.accommodation_id.seq_no')
    acco_id = fields.Char()
    quantity = fields.Integer(string="Quantity", store="True")
    image_view = fields.Image(related='food_id.image')
    food_id = fields.Many2one('room.food')
    description_view = fields.Text(related='food_id.description')
    price_view = fields.Float(compute=_compute_price)
    subtotal_price = fields.Float(compute=_compute_subtotal_price,
                                  string="Subtotal")
    rent = fields.Boolean(default=False)
    amount_total = fields.Float()
    category_view = fields.Char()
    name = fields.Char()
    order = fields.Boolean(default=False)
    uom_id = fields.Many2one('uom.uom', string="UoM")

    def add_to_list(self):
        """Add to list"""
        for rec in self.food_id:
            print("Food Id:", rec.id)
        for rec in self:
            columns = {
                'acco_id': rec.acco_id,
                'orders_id': rec.orders_id,
                # 'food_id': rec.id,
                'name': rec.food_name,
                'quantity': rec.quantity,
                'order': '1',
                'uom_id': rec.uom_id.id,
                # 'food_name': rec.food_name,
                'description': rec.description,
                'rent': 'False',
                'price': rec.price
                }
        print("Out test: ", columns)
        self.order_id.orders = columns
        # print("Id :", )
        self.env['room.food'].create(columns)


class FoodCategory(models.Model):
    _name = 'food.category'
    _description = 'Food category'
    _rec_name = 'category_name'

    category_name = fields.Char(string="Category", required="True")