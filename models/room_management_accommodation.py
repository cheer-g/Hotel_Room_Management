# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Accommodation(models.Model):
    _name = 'room.accommodation'
    _description = 'Room Accommodation'
    _inherit = 'mail.thread'
    _rec_name = 'seq_no'

    def _compute_amount_total(self):
        if self.orders_ids:
            for rec in self.orders_ids:
                self.amount_total += rec.subtotal_price
        else:
            self.amount_total = 0

    def _compute_invoice_id(self):
        """get invoice and check status"""
        for rec in self:
            result = self.env['account.move'].search([
                ('name', '=', rec.seq_no)
            ])
            self.update({'invoice_id': result})
        self.update({'paid_state': self.invoice_id.payment_state})

    def _compute_rent(self):
        """Compute rent based on no. of days"""
        for rec in self:
            if rec.check_in:
                if rec.check_out:
                    init_date = rec.check_in.strftime("%Y-%m-%d")
                    end_date = rec.check_out.strftime("%Y-%m-%d")
                    checkin_date = datetime.strptime(init_date, '%Y-%m-%d')
                    checkout_date = datetime.strptime(end_date, '%Y-%m-%d')
                    days = str((checkout_date - checkin_date).days)
                    rec.days_stay = (int(days) + 1)
                    rent = (int(days) + 1) * rec.room_no_id.rent
                else:
                    init_date = rec.check_in.strftime("%Y-%m-%d")
                    end_date = fields.Datetime.today().strftime("%Y-%m-%d")
                    checkin_date = datetime.strptime(init_date, '%Y-%m-%d')
                    checkout_date = datetime.strptime(end_date, '%Y-%m-%d')
                    days = str((checkout_date - checkin_date).days)
                    rec.days_stay = int(days) + 1
                    rent = (int(days) + 1) * rec.room_no_id.rent
            else:
                rent = rec.room_no_id.rent
            self.update({'rent': rent})
            self.update({'rent_amount': rent})
            result = self.env['room.food'].search([
                ('name', '=', 'Rent'), ('accommodation_id', '=', self.id)
            ])
            result.quantity = self.days_stay

    def _compute_orders_count(self):
        for rec in self:
            lists = self.env['order.food'].search([
                ('accommodation_id', '=', rec.seq_no)])
            rec.orders_count = len(lists)

    seq_no = fields.Char(string="Sequence No.", required="True",
                         readonly="True", copy="False",
                         index="True", default=lambda self: 'New')
    guest_id = fields.Many2one(
        'res.partner', string='Guests',
        required=True, index=True, tracking=1)
    guest_count = fields.Integer(required="True", default="1")
    check_in = fields.Datetime(readonly="True")
    check_out = fields.Datetime(readonly="True")
    expected_days = fields.Integer(string="Expected Days", default="1")
    expected_date = fields.Date(string="Expected Date",
                                readonly=True, default=fields.Date.today())
    bed = fields.Selection(selection=[('single', 'Single'),
                                      ('double', 'Double'),
                                      ('dormitory', 'Dormitory')],
                           default='single', required="True")
    facilities_ids = fields.Many2many('room.facilities', string="Facilities")
    room_no_id = fields.Many2one('room.management',
                                 string="Room", required="True",
                                 change_default="True",
                                 domain="[('state','=','available')]")
    add_guest_ids = fields.One2many('room.guests', 'guest_ids')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True)
    rent = fields.Float(string="Rent", compute=_compute_rent)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'Check-In'),
        ('checkout', 'Check-Out'),
        ('cancel', 'Cancelled'),
        ('paid', 'Paid')], string="Status", readonly="True", default="draft",
        tracking=1, tracking_visibility='always')
    current_date = fields.Datetime(default=fields.Date.today())
    # food_order_ids = fields.One2many('food.menu', 'accommodation_id',
    #                                  readonly="False",
    #                                  domain=[('accommodation_id', '=',
    #                                           seq_no)])
    orders_ids = fields.One2many('room.food', 'accommodation_id',
                                 domain=[('order', '=', 'True')])
                                 # compute=_compute_orders_id)
    orders_count = fields.Integer(compute=_compute_orders_count)
    days_stay = fields.Integer()
    invoice_id = fields.Many2one('account.move', compute=_compute_invoice_id)
    paid_state = fields.Char(compute=_compute_invoice_id)
    amount_total = fields.Float(compute=_compute_amount_total, string="Total")
    rent_amount = fields.Float(default='0')

    @api.onchange('expected_days')
    def _onchange_expected_date(self):
        """
         Computing expected date based on expected days
        """
        if self.expected_days:
            self.expected_date = fields.Datetime.now() + \
                                 timedelta(self.expected_days - 1)
        else:
            self.expected_date = fields.Date.today()

    @api.onchange('bed')
    def _onchange_bed(self):
        self.room_no_id = False
        if not self.facilities_ids:
            return {'domain': {
                'room_no_id': [('bed', '=', self.bed),
                               ('state', '=', 'available')]}}

    @api.onchange('facilities_ids')
    def onchange_facilities(self):
        """
        For displaying room number based on Bed type and Facilities
        """
        if self.facilities_ids:
            return {'domain': {'room_no_id': [('bed', '=', self.bed),
                                              ('facility.id', 'in',
                                               self.facilities_ids.ids),
                                              ('state', '=', 'available')]}}

    @api.onchange('room_no_id')
    def _onchange_room_no_id(self):
        result = self.env['room.facilities'].search([
            ('id', 'in', self.room_no_id.facility.ids)
        ])
        self.rent = self.room_no_id.rent
        self.update({'facilities_ids': result})

    @api.model
    def create(self, vals):
        """
        To Generate Sequence number
        """
        if vals.get('seq_no', 'New') == 'New':
            vals['seq_no'] = self.env['ir.sequence'].next_by_code(
                'acc.seq') or 'New'
        result = super(Accommodation, self).create(vals)
        return result

    def action_checkin(self):
        """
         Change state to checkin and update check_in field using Confirm button
        """
        for rec in self:
            guest_count_list = 1 + len(self.add_guest_ids.ids)
            if not self.message_main_attachment_id.id:
                rec.state = 'draft'
                raise UserError(
                    _('Please provide address proof'))
            if guest_count_list == rec.guest_count:
                self.room_no_id.state = 'not-available'
                self.room_no_id.accommodation_seq = rec.seq_no
                self.check_in = fields.Datetime.now()
                rec.state = 'checkin'
                rent = rec.rent
            else:
                rec.state = 'draft'
                raise UserError(
                    _('Please provide all guests details'))

        rent_product = self.env['product.product'].search([
            ('name', '=', 'Rent')])
        rent_uom = self.env['room.food'].search(
            [('food_name', '=', 'Rent')])
        columns = {
            'accommodation_id': self.id,
            'product_id': rent_product.id,
            'quantity': self.days_stay,
            'name': "Rent",
            'description': "Rent",
            'uom_id': rent_uom.uom_id.id,
            'order': 'True',
            'rent': 'True',
            'price': rent}
        self.env['room.food'].create(columns)  # Creating a record for rent

    def action_checkout(self):
        """
        Makes the room available and change state to checkout
        """
        for rec in self:
            rec.room_no_id.state = 'available'
            rec.room_no_id.accommodation_seq = 'Not Assigned'
            rec.state = 'checkout'
            rec.check_out = fields.Datetime.now()

        """Create Customer invoice"""
        invoice_lines = []
        for rec in self.orders_ids:
            line = (0, 0, {
                'product_id': rec.product_id,
                'name': rec.name,
                'price_unit': rec.price,
                'quantity': rec.quantity,
                'discount': 0.0,
            })
            invoice_lines.append(line)
        for rec in self:
            invoice_line = self.env['account.move'].create({
                'partner_id': self.guest_id.id,
                'currency_id': self.currency_id.id,
                'l10n_in_gst_treatment': 'consumer',
                'name': self.seq_no,
                'state': 'draft',
                'move_type': 'out_invoice',
                'invoice_date': self.check_out,
                # 'account_id': self.account_receivable.id,
                'invoice_line_ids': invoice_lines,
            })
            # invoice_line.action_post()
            return {
                'name': 'Customer Invoice',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': invoice_line.id
            }

    def action_cancel(self):
        """
        Makes the room available and change state to cancel
        """
        for rec in self:
            rec.state = 'cancel'
            self.room_no_id.accommodation_seq = 'Not Assigned'
            self.room_no_id.state = 'available'

    def get_orders(self):
        """Smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree,form',
            'res_model': 'order.food',
            'domain': [('accommodation_id', '=', self.id)],
            'context': "{'create': False}"
        }


class AdditionalGuests(models.Model):
    _name = 'room.guests'
    _description = 'Additional Guests'
    _rec_name = 'add_guest_name'

    guest_ids = fields.Many2one('room.accommodation')
    add_guest_name = fields.Char(string="Guest Name", required="True")
    add_guest_gender = fields.Selection(selection=[('male', 'Male'),
                                                   ('female', 'Female'),
                                                   ('other', 'Other')],
                                        string='Gender')
    add_guest_age = fields.Integer(string="Age")
