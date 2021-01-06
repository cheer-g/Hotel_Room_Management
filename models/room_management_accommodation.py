# -*- coding: utf-8 -*-

import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Accommodation(models.Model):
    _name = 'room.accommodation'
    _description = 'Room Accommodation'
    _inherit = 'mail.thread'
    _rec_name = 'seq_no'

    seq_no = fields.Char(string="Sequence No.", required="True",
                         readonly="True", copy="False",
                         index="True", default=lambda self: 'New')
    guest_id = fields.Many2one(
        'res.partner', string='Guests',
        required=True, index=True, tracking=1)
    guest_count = fields.Integer(required="True", default="1")
    attachment_ids = fields.Many2many('ir.attachment',
                                      'address_attachment_rel', 'address_id',
                                      'attachment_id', string='Attachments')
    check_in = fields.Datetime(readonly="True")
    check_out = fields.Datetime(readonly="True")
    expected_days = fields.Integer(string="Expected Days")
    expected_date = fields.Date(string="Expected Date",
                                readonly=True)
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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'Check-In'),
        ('checkout', 'Check-Out'),
        ('cancel', 'Cancelled')
    ], string="Status", readonly="True",
        default="draft", tracking=1, tracking_visibility='always')
    current_date = fields.Datetime(default=fields.Date.today())
    food_order_ids = fields.One2many('order.food', 'order_sequence',
                                     readonly="False")

    @api.onchange('expected_days')
    def _compute_expected_date(self):
        """
         Computing expected date based on expected days
        """
        for rec in self:
            if rec.expected_days:
                rec.expected_date = fields.Date.today() + datetime.timedelta(
                    rec.expected_days)
            else:
                rec.expected_date = fields.Date.today()

    @api.onchange('bed')
    def _onchange_bed(self):
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
            print({'domain': {'room_no_id': [('bed', '=', self.bed),
                                              ('facility.id', 'in',
                                               self.facilities_ids.ids),
                                              ('state', '=', 'available')]}})
            return {'domain': {'room_no_id': [('bed', '=', self.bed),
                                              ('facility.id', 'in',
                                               self.facilities_ids.ids),
                                              ('state', '=', 'available')]}}

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

    # @api.onchange('expected_days')
    # def _compute_expected_date(self):
    #     """
    #      Computing expected date based on expected days
    #     """
    #     today = fields.Date.today()
    #     self.expected_date = today + datetime.timedelta(days=self.expected_days)

    def action_checkin(self):
        """
         Change state to checkin and update check_in field using Confirm button
        """
        for rec in self:
            guest_count_list = 1 + len(self.add_guest_ids.ids)
            if not self.attachment_ids:
                rec.state = 'draft'
                raise UserError(
                    _('Please provide address proof'))
            if guest_count_list == rec.guest_count:
                self.room_no_id.state = 'not-available'
                self.room_no_id.accommodation_seq = rec.seq_no
                self.check_in = fields.Datetime.now()
                rec.state = 'checkin'
            else:
                rec.state = 'draft'
                raise UserError(
                    _('Please provide all guests details'))

    def action_checkout(self):
        """
        Makes the room available and change state to checkout
        """
        for rec in self:
            self.room_no_id.state = 'available'
            self.room_no_id.accommodation_seq = 'Not Assigned'
            rec.state = 'checkout'
            self.check_out = fields.Datetime.now()

    def action_cancel(self):
        """
        Makes the room available and change state to cancel
        """
        for rec in self:
            rec.state = 'cancel'
            self.room_no_id.accommodation_seq = 'Not Assigned'
            self.room_no_id.state = 'available'


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
