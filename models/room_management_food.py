# -*- coding : utf-8 -*-

from odoo import models, fields


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
    orders_id = fields.Char()
    accommodation_id = fields.Many2one('room.food')
    acco_id = fields.Char()
    quantity = fields.Integer(string="Quantity", store="True")
    image_view = fields.Image(related='food_id.image')
    food_id = fields.Many2one('room.food')
    product_id = fields.Integer()
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
    tax_ids = fields.Many2many('account.tax')

    def add_to_list(self):
        """Add to list"""
        food_product = self.env['product.product'].search([
            ('name', '=', 'Food Item')])

        for rec in self:
            order = self.env['order.food'].search([
                ('order_sequence', '=', rec.orders_id)])
            print("Orderr :", order.id)
            columns = {
                'accommodation_id': rec.accommodation_id.id,
                'order_id': order.id,
                'product_id': food_product.id,
                'name': rec.food_name,
                'quantity': rec.quantity,
                'order': '1',
                'uom_id': rec.uom_id.id,
                # 'food_name': rec.food_name,
                'description': rec.description,
                'rent': 'False',
                'price': rec.price,
                'tax_ids': rec.tax_ids.ids
                }
            print("Orderrrr : ", rec.orders_id)
        # self.order_id.orders = columns
        self.env['room.food'].create(columns)


class FoodCategory(models.Model):
    _name = 'food.category'
    _description = 'Food category'
    _rec_name = 'category_name'

    category_name = fields.Char(string="Category", required="True")
