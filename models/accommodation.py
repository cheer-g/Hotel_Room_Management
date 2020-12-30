"""
Model for the accommodation view
"""
# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api


class Accommodation(models.Model):
    """
    Class for the Accommodation view
    """
    _name = 'room.accommodation'
    _description = 'Room Accommodation'
    _inherit = 'mail.thread'
    _rec_name = 'seq_no'

    seq_no = fields.Char(string="Sequence No.", required="True",
                         readonly="True", copy="False",
                         index="True", default=lambda self: 'New')
    guest = fields.Many2one(
        'res.partner', string='Guests',
        required=True, change_default=True, index=True, tracking=1)
    # address_proof_ids = fields.Binary('Address Proof')
    # address_proof_id = fields.One2many('ir.attachment', 'attach_id',
    #                                    string="Address Proof", copy="False")
    guest_count = fields.Integer(required="True", default="1")
    attachment_ids = fields.Many2many('ir.attachment',
                                      'address_attachment_rel', 'address_id',
                                      'attachment_id', string='Attachments')
    check_in = fields.Datetime(readonly="True")
    check_out = fields.Datetime(readonly="True")
    expected_days = fields.Integer(string="Expected Days")
    expected_date = fields.Date(string="Expected Date",
                                readonly=True,
                                compute="_compute_expected_date")
    bed = fields.Selection(selection=[('single', 'Single'),
                                      ('double', 'Double'),
                                      ('dormitory', 'Dormitory')],
                           default='single', required="True")
    facilities = fields.Many2many('room.facilities', string="Facilities")
    room_no = fields.Many2one('room.management',
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

    @api.onchange('facilities')
    def onchange_facilities(self):
        """
        For displaying room number based on Bed type and Facilities

        """
        for rec in self:
            print("Out : ", rec.facilities.ids)
            return {'domain': {'room_no': [('bed', '=', self.bed),
                                           ('facility.id', 'in',
                                            rec.facilities.ids),
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

    @api.onchange('expected_days')
    def _compute_expected_date(self):
        """
         Computing expected date based on expected days
        """
        today = fields.Date.today()
        self.expected_date = today + datetime.timedelta(
            days=self.expected_days)

    def action_checkin(self):
        """
         Change state to checkin and update check_in field using Confirm button
        """
        for rec in self:
            guest_count_list = 1 + len(self.add_guest_ids.ids)
            if not self.attachment_ids:
                rec.state = 'draft'
                print("Add address proof")
                warning = {
                    'name': 'No address proof found !',
                    'type': 'ir.actions.act_window',
                    'res_model': 'address.warning',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'target': 'new'
                }
                return warning
            if guest_count_list == rec.guest_count:
                self.room_no.state = 'not-available'
                self.check_in = fields.Datetime.now()
                rec.state = 'checkin'
            else:
                rec.state = 'draft'
                print('Please provide all guests details')
                warning = {
                    'name': 'Guest count mismatch !',
                    'type': 'ir.actions.act_window',
                    'res_model': 'guest.count.warning',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'target': 'new'
                }
                return warning

    def action_checkout(self):
        """
        Makes the room available and change state to checkout
        """
        for rec in self:
            self.room_no.state = 'available'
            rec.state = 'checkout'
            self.check_out = fields.Datetime.now()

    def action_cancel(self):
        """
        Makes the room available and change state to cancel
        """
        for rec in self:
            rec.state = 'cancel'
            self.room_no.state = 'available'


class AdditionalGuests(models.Model):
    """
    Class for the tree view under accommodation form
    """
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


class GuestWarning(models.TransientModel):
    """
    Class for Guest count mismatch warning view
    """
    _name = 'guest.count.warning'
    _description = 'Guest count Warning'

    guest_count_warning = fields.Text(
        string="Please provide all guests details",
        readonly=True, store=True)
    address_proof_warning = fields.Text(
        string="Please provide address proof",
        readonly=True, store=True)


class AddressWarning(models.TransientModel):
    """
    Class for No address proof warning
    """
    _name = 'address.warning'
    _description = 'No address proof Warning'

    address_proof_warning = fields.Text(
        string="Please provide address proof",
        readonly=True, store=True)
