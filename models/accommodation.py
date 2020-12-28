# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Accommodation(models.Model):
    _name = 'room_management.accommodation'
    _description = 'room_accommodation'
    _rec_name = 'seq_no'
    # _inherit = 'res.partner'

    is_invoice_contact = fields.Boolean("Is Invoice contact?")
    seq_no = fields.Char(string="Reference No.", required="True", readonly="True", copy="False",
                         index="True", default=lambda self: 'New')
    guest = fields.Many2one(
        'res.partner', string='Guests', readonly=False,
        required=True, change_default=True, index=True, tracking=1)
    guest_address = fields.Many2one(
        'res.partner', string='Address', required=True)
    guest_count = fields.Integer(required="True")
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    bed = fields.Selection(selection=[('single', 'Single'), ('double', 'Double'), ('dorm', 'Dormitory')])
    facilities = fields.Many2many('room_management.facilities', string="Facilities")
    room_no = fields.Many2one('room.management',
                              string="Room", required="True", change_default="True")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checkin', 'Check-In'),
        ('checkout', 'Check-Out'),
        ('cancel', 'Cancelled')
    ], string="Status", readonly="True", default="draft")

    @api.onchange('guest')
    def onchange_guest(self):
        for rec in self:
            print("Output check : ", rec.guest.street)
            return {'domain': {'guest_address': [('id', '=', rec.guest.id)]}}

    @api.onchange('room_no')
    def onchange_room_no(self):
        for rec in self:
            print("Output check 2: ", rec.room_no.room_no)
            return {'domain': {'facilities': [('room_no.room_no', '=', rec.room_no.room_no)]}}

    @api.model
    def create(self, vals):
        if vals.get('seq_no', 'New') == 'New':
            vals['seq_no'] = self.env['ir.sequence'].next_by_code('acc.seq') or 'New'
        result = super(Accommodation, self).create(vals)
        return result

    def action_confirm(self):
        for rec in self:
            rec.state = 'checkin'

    def action_checkout(self):
        for rec in self:
            rec.state = 'checkout'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class Test(models.Model):
    _name = 'room.accommodation'


class Test1(models.Model):
    _name = 'room_management.room_management'
