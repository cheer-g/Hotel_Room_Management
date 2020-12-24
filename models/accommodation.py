# -*- coding: utf-8 -*-

from odoo import models, fields


class Accommodation(models.Model):
    _name = 'room_management.accommodation'
    _description = 'room_accommodation'
    STATE_SELECTION = [('draft', 'Draft')]

    ref_no = fields.Char(readonly="True")
    guest = fields.Many2one('res.partners', 'Guests')
    guest_count = fields.Integer(required="True")
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    bed = fields.Selection(selection=[('single', 'Single'), ('double', 'Double'), ('dorm', 'Dormitory')])
    facilities = fields.Text()
    room_no = fields.Integer(required="True")

class Test(models.Model):
    _name = 'room.accommodation'

class Test1(models.Model):
    _name = 'room_management.room_management'
