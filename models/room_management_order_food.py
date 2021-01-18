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
        ('cancel', 'Cancelled')], string="Status", readonly="True",
        default="draft", tracking=1, tracking_visibility='always')

    @api.onchange('room_no_id')
    def _onchange_room_no_id(self):
        """
        Function to retrieve the corresponding accommodation entry
        """
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
        result.order = 0
        self.update({'product_ids': result})

    def get_accommodation(self):
        """For smart button"""
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
        # result = self.env['room.food'].search(
        #     [('category_id', '=', False)])
        # result.orders_id = False
        # result.acco_id = False
        for rec in self:
            rec.state = 'ordered'

    def action_cancel(self):
        """Action for cancel button"""
        for rec in self:
            result = self.env['room.food'].search([
                ('orders_id', '=', rec.order_sequence), ('order', '=', '1')])
            result.acco_id = 'False'
            rec.state = 'cancel'
