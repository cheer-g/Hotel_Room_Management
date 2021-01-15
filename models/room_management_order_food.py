# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrderFood(models.Model):
    _name = 'order.food'
    _description = 'Order Food'
    _rec_name = 'order_sequence'
    _inherit = 'mail.thread'

    def _compute_order_ids(self):
        for rec in self:
            result = self.env['room.food'].search([
                ('orders_id', '=', rec.order_sequence),
                ('order', '=', 'True')])
            print("Result :", result)
            rec.update({'order_ids': result})

    # Order details
    order_sequence = fields.Char(string="Order No.", required="True",
                                 readonly="True", copy="False",
                                 index="True", default=lambda self: 'New')
    room_no_id = fields.Many2one('room.management',
                                 domain=[('state', '=', 'not-available')],
                                 required=True, string="Room No.")
    accommodation_id = fields.Many2one('room.accommodation')
    guest_id = fields.Many2one('res.partner', string="Guest")
    order_time = fields.Datetime(string="Order Time")

    # Food details
    category_ids = fields.Many2many('food.category', string='Category',
                                    required=True,
                                    domain=[('category_name', '!=', 'Rent')])
    product_ids = fields.Many2many('room.food', string='Product')
    order_ids = fields.One2many('room.food', 'order_id',
                                compute=_compute_order_ids)
    orders = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ordered', 'Ordered'),
        ('cancel', 'Cancelled')
    ], string="Status", readonly="True",
        default="draft", tracking=1, tracking_visibility='always')

    @api.onchange('room_no_id')
    def _onchange_room_no_id(self):
        """
        Function to retrieve the corresponding accommodation entry
        """
        print("Output : ", self.accommodation_id.guest_id.id)
        result_id = self.env['room.accommodation'].search([
            ('seq_no', '=', self.room_no_id.accommodation_seq)])
        self.update({'accommodation_id': result_id})
        self.order_time = fields.Datetime.now()

    @api.onchange('accommodation_id')
    def _onchange_accommodation_id(self):
        """
        Function to retrieve corresponding guest
        """
        self.update({'guest_id': self.accommodation_id.guest_id.id})

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

    @api.onchange('category_ids')
    def _onchange_category_ids(self):
        """
        To retrieve lunch products based on category
        """
        result = self.env['room.food'].search(
            [('category_id', 'in', self.category_ids.ids)])
        result.orders_id = self.order_sequence
        result.acco_id = self.accommodation_id.seq_no
        result.quantity = '1'
        # print("test : ", result.accommodation_id)
        self.update({'product_ids': result})
        # return {'product_ids': result}

    def get_accommodation(self):
        print("Acco :", self.accommodation_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accommodation',
            'res_model': 'room.accommodation',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.accommodation_id.id)],
            'context': " {'create': False, 'create_edit': False}"
        }

    def action_order(self):
        """Action for order button"""
        for rec in self:
            rec.state = 'ordered'

    def action_cancel(self):
        """Action for cancel button"""
        for rec in self:
            rec.state = 'cancel'

    def add_to_list(self):
        """
           Add to list function
        """
        print("View check")
        form_view_id = self.env.ref("room_management.order_view_form").id
        return {
            'name': 'Add to list',
            'type': 'ir.actions.act_window',
            'res_model': 'room.food',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'target': 'new'
        }


class FoodMenu(models.Model):
    _name = 'food.menu'
    _description = 'Food Menu'
    # _rec_name = 'food_id'

    food_id = fields.Many2one('room.food')
    quantity = fields.Integer(default="1")

    def add_to_list(self):
        """Add to List"""
        vals = {
            'food_id': self.food_id,
            'quantity': self.quantity
        }
        self.env['room.food'].create(vals)

    # def _compute_subtotal_price(self):
    #     """
    #     Compute total price based on the quantity ordered
    #     """
    #     # print("Acco :", self.accommodation_entry)
    #     for rec in self:
    #         rec.subtotal_price = rec.price * rec.quantity
    #
    # def _compute_price(self):
    #     """Compute item price"""
    #     for rec in self:
    #         if not rec.rent:
    #             rec.update({'price': rec.food_id.price})
    #         else:
    #             rec.price = 0
    # order_id = fields.Many2one('order.food')
    # accommodation_id = fields.Many2one('room.accommodation',
    #                                       related='order_id.accommodation_id',
    #                                    string="Accommodation ID")
    # quantity = fields.Integer(string="Quantity", default='1')
    # image = fields.Image(related='food_id.image')
    # food_id = fields.Many2one('room.food')
    # description = fields.Text(related='food_id.description')
    # currency_id = fields.Many2one(
    #     'res.currency', string='Currency',
    #     default=lambda self: self.env.user.company_id.currency_id.id,
    #     required=True)
    # price = fields.Float(compute=_compute_price)
    # subtotal_price = fields.Float(compute=_compute_subtotal_price,
    #                               string="Subtotal")
    # rent = fields.Boolean(default=False)
    # amount_total = fields.Float()
    # category_id = fields.Char()
    #
    # def add_to_list(self):
    #     """
    #        Add to list function
    #     """
    #     print("View check")
    #     return {
    #         'name': 'Add to list',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'food.menu',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'target': 'new'
    #     }
