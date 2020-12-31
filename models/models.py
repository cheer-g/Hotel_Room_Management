"""
Model for the room view
"""
# -*- coding: utf-8 -*-

from odoo import models, fields
# from . import facilities


class RoomManagement(models.Model):
    """
    Class for the room management view
    """
    _name = 'room.management'
    _description = 'room_management'
    _rec_name = 'room_no'

    room_no = fields.Char(required="True")
    bed = fields.Selection(selection=[('single', 'Single'),
                                      ('double', 'Double'),
                                      ('dormitory', 'Dormitory')],
                           default='single')
    total_bed = fields.Integer()
    facility = fields.Many2many('room.facilities', string="Facilities")
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True)
    rent = fields.Monetary(string="Rent")
    state = fields.Selection(selection=[('available', 'Available'),
                                        ('not-available', 'Not Available')],
                             string="Status", readonly="True",
                             default='available')
    accommodation_seq = fields.Char(readonly="True")
    _sql_constraints = [
        ('Room_no', 'unique (room_no)', 'This Room No. Already exist!')]
