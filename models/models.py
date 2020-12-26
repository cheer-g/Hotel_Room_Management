# -*- coding: utf-8 -*-

from odoo import models, fields
from . import facilities


class RoomManagement(models.Model):
    _name = 'room.management'
    _description = 'room_management'
    _rec_name = 'room_no'

    room_no = fields.Integer(required="True")
    bed = fields.Selection(selection=[('single', 'Single'), ('double', 'Double'), ('dorm', 'Dormitory')])
    total_bed = fields.Integer()
    facility = fields.Many2many('room_management.facilities', string="Facilities")
    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    rent = fields.Monetary('Rent', currency_field='currency_id')

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
