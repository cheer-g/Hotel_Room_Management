# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrderFood(models.Model):
    _name = 'order.food'
    _description = 'Order Food'
    _rec_name = 'order_sequence'

    # Order details
    order_sequence = fields.Char(string="Order No.", required="True",
                                 readonly="True", copy="False",
                                 index="True", default=lambda self: 'New')
    room_no_id = fields.Many2one('room.management',
                                 domain=[('state', '=', 'not-available')],
                                 required=True, string="Room No.")
    accommodation_entry = fields.Many2one('room.accommodation')
    guest_id = fields.Many2one('res.partner', string="Guest")
    order_time = fields.Datetime(string="Order Time")

    # Food details
    category_ids = fields.Many2many('food.category', string='Category',
                                    required=True)
    product_ids = fields.Many2many('room.food', string='Product',
                                   readonly="False")
    name = fields.Char('Product Name', related='product_ids.food_name')
    price = fields.Float(string="Price")
    image = fields.Image(related='product_ids.image')
    quantity = fields.Integer(string="Quantity")
    order_ids = fields.One2many('food.menu', 'order_id')

    @api.onchange('room_no_id')
    def _onchange_room_no_id(self):
        """
        Function to retrieve the corresponding accommodation entry
        """
        print("Output : ", self.accommodation_entry.guest_id.id)
        result_id = self.env['room.accommodation'].search([
            ('seq_no', '=', self.room_no_id.accommodation_seq)])
        self.update({'accommodation_entry': result_id})
        self.order_time = fields.Datetime.now()

    @api.onchange('accommodation_entry')
    def _onchange_accommodation_entry(self):
        """
        Function to retrieve corresponding guest
        """
        result_id = self.env['res.partner'].search([
            ('id', '=', self.accommodation_entry.guest_id.id)], limit=1)
        print("Test", result_id.id)
        self.update({'guest_id': result_id.id})

    @api.model
    def create(self, vals):
        """
        To Generate Sequence number
        """
        if vals.get('order_sequence', 'New') == 'New':
            vals['order_sequence'] = self.env['ir.sequence'].next_by_code(
                'order.seq') or 'New'
        result = super(OrderFood, self).create(vals)
        self.accommodation_entry.food_order_ids = result
        return result

    @api.onchange('category_ids')
    def _onchange_category_ids(self):
        """
        To retrieve lunch products based on category
        """
        # print("Testtest : ", rec.category_ids.ids)
        # return {'domain': {'product_ids':
        #                        [('category_id', 'in',
        #                          rec.category_ids.ids)]}}

        pack_id = self.env['room.food'].search(
            [('category_id', 'in', self.category_ids.ids)])
        print("test : ", pack_id)
        self.update({'product_ids': pack_id})

    def add_to_list(self):
        """
           Add to list function
        """
        print("View check")
        return {
            'name': 'Add to list',
            'type': 'ir.actions.act_window',
            'res_model': 'food.menu',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }


class FoodMenu(models.Model):
    _name = 'food.menu'
    _description = 'Food Menu'

    def _compute_subtotal_price(self):
        for rec in self:
            rec.subtotal_price = rec.price * rec.quantity

    def _compute_accommodation_entry(self):
        for rec in self:
            print(self.accommodation_entry)
            return {'domain': {'accommodation_entry':[
                ('accommodation_entry', '=', rec.order_id.accommodation_entry)
            ]}}

    order_id = fields.Many2one('order.food')
    accommodation_entry = fields.Many2one('room.accommodation',
                                          default=_compute_accommodation_entry)
    quantity = fields.Integer(string="Quantity", default='1')
    image = fields.Image()
    food_name = fields.Many2one('room.food')
    price = fields.Float(related='food_name.price')
    subtotal_price = fields.Float(compute=_compute_subtotal_price,
                                  string="Subtotal")
    amount_total = fields.Float()
    category_id = fields.Char()

    def add_to_list(self):
        """
           Add to list function
        """
        print("View check")
        return {
            'name': 'Add to list',
            'type': 'ir.actions.act_window',
            'res_model': 'food.menu',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }

