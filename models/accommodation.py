# -*- coding: utf-8 -*-

"""
 Model for Accommodation view
"""
import datetime
from odoo import models, fields, api


class Accommodation(models.Model):
    _name = 'room.accommodation'
    _description = 'room_accommodation'
    _rec_name = 'seq_no'

    seq_no = fields.Char(string="Sequence No.", required="True",
                         readonly="True", copy="False",
                         index="True", default=lambda self: 'New')
    guest = fields.Many2one(
        'res.partner', string='Guests', readonly=False,
        required=True, change_default=True, index=True, tracking=1)
    address_proof = fields.Binary('Address Proof')
    guest_count = fields.Integer(required="True")
    check_in = fields.Datetime(readonly="True")
    check_out = fields.Datetime(readonly="True")
    expected_days = fields.Integer(string="Expected Days")
    expected_date = fields.Date(string="Expected Date",
                                readonly=True,
                                compute="calc_date")
    bed = fields.Selection(selection=[('single', 'Single'),
                                      ('double', 'Double'),
                                      ('dormitory', 'Dormitory')],
                           default='single', required="True")
    facilities = fields.Many2many('room.facilities', string="Facilities")
    room_no = fields.Many2one('room.management',
                              string="Room", required="True",
                              change_default="True")
    add_guests = fields.One2many('room.guests', 'add_guest_name')
    # room_no = fields.Char(compute='depends_bed')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'Check-In'),
        ('checkout', 'Check-Out'),
        ('cancel', 'Cancelled')
    ], string="Status", readonly="True", default="draft")

    # For displaying facilities according to the room number
    @api.onchange('room_no')
    def onchange_room_no(self):
        for rec in self:
            print("Output check 2: ", rec.room_no.room_no)
            return {'domain': {'facilities': [
                ('room_no.room_no', '=', rec.room_no.room_no)]}}

    # @api.depends('bed')
    # def depends_bed(self):
    #     print("Bed type: ", self.bed)
    #     room_no = fields.Many2one('room.management',
    #                               string="Room", required="True",
    #                               change_default="True",
    #                               domain="[('bed', '=', self.bed)]")

    # To Generate Sequence number
    @api.model
    def create(self, vals):
        if vals.get('seq_no', 'New') == 'New':
            vals['seq_no'] = self.env['ir.sequence'].next_by_code(
                'acc.seq') or 'New'
        result = super(Accommodation, self).create(vals)
        return result

    @api.onchange('expected_days')
    def calc_date(self):
        today = fields.Date.today()
        self.expected_date = today + datetime.timedelta(
            days=self.expected_days)

    # Change state to checkin and update check_in field using Confirm button
    def action_confirm(self):
        for rec in self:
            rec.state = 'checkin'
            self.check_in = fields.Datetime.now()

    def action_checkout(self):
        for rec in self:
            rec.state = 'checkout'
            self.check_out = fields.Datetime.now()

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class AdditionalGuests(models.Model):
    _name = 'room.guests'
    _description = 'Additional Guests'
    _rec_name = 'add_guest_name'

    guests_list = fields.Many2one('room.accommodation', 'add_guests')
    add_guest_name = fields.Char(string="Guest Name")
    add_guest_gender = fields.Selection(selection=[('male', 'Male'),
                                                   ('female', 'Female'),
                                                   ('other', 'Other')],
                                        string='Gender')
    add_guest_age = fields.Integer(string="Age")
