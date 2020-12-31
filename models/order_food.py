"""
For order food Menu
"""
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrderFood(models.Model):
    """
    Class for Order food menu
    """
    _name = 'order.food'
    _description = 'Order Food'
    _rec_name = 'order_sequence'

    # Order details
    order_sequence = fields.Char(string="Order No.", required="True",
                                 readonly="True", copy="False",
                                 index="True", default=lambda self: 'New')
    room_no_id = fields.Many2one('room.management',
                                 domain=[('state', '=', 'not-available')])
    accommodation_entry = fields.Many2one('room.accommodation', required="true",
                                          limit=1)
    guest_id = fields.Many2one('res.partner')
    order_time = fields.Datetime(default=fields.Datetime.now(), readonly="True")

    # Food details
    category_id = fields.Many2one('lunch.product.category',
                                  string='Product Category',
                                  required=True)
    product_ids = fields.Many2many('lunch.product', string='Product')
    name = fields.Char('Product Name', related='product_ids.name')
    price = fields.Float('Price')

    image_1920 = fields.Image(compute='_compute_product_images')
    image_128 = fields.Image(compute='_compute_product_images')

    def _compute_image(self):
        for line in self:
            line.image_1920 = line.product_id.image_1920 or line.category_id.image_1920
            line.image_128 = line.product_id.image_128 or line.category_id.image_128

    @api.onchange('room_no_id')
    def _onchange_room_no_id(self):
        """
        Function to retrieve the corresponding accommodation entry
        """
        for rec in self:
            print("Output : ", rec.accommodation_entry.guest_id.id)
            return {'domain':
                {'accommodation_entry':
                    [(
                        'seq_no', '=', rec.room_no_id.accommodation_seq)]}}

    @api.onchange('accommodation_entry')
    def _onchange_accommodation_entry(self):
        """
        Function to retrieve corresponding guest
        """
        for rec in self:
            return {'domain': {
                'guest_id': [('id', '=', rec.accommodation_entry.guest_id.id)]}}

    @api.model
    def create(self, vals):
        """
        To Generate Sequence number
        """
        if vals.get('order_sequence', 'New') == 'New':
            vals['order_sequence'] = self.env['ir.sequence'].next_by_code(
                'order.seq') or 'New'
        result = super(OrderFood, self).create(vals)
        return result

    @api.onchange('category_id')
    def _onchange_category_id(self):
        """
        To retrieve lunch products based on category
        """
        for rec in self:
            return {'domain': {'product_ids':
                                   [('category_id.id', '=',
                                     rec.category_id.id)]}}


class FoodMenu(models.Model):
    _name = 'food.menu'
    _description = 'Food Menu'
    _inherit = 'order.food'

    price = fields.Float(string="Price")
    quantity = fields.Integer(string="Quantity")

    def add_to_cart(self):
        """
            Useless function
        """
        for rec in self:
            if rec.category_id:
                return {
                    'name': 'Food !',
                    'type': 'ir.actions.act_window',
                    'res_model': 'food.menu',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'target': 'new'
                }
