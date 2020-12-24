# -*- coding: utf-8 -*-

from odoo import models, fields
from . import facilities


class RoomManagement(models.Model):
    _name = 'room.management'
    _description = 'room_management'

    room_no = fields.Integer(required="True")
    bed = fields.Selection(selection=[('single', 'Single'), ('double', 'Double'), ('dorm', 'Dormitory')])
    total_bed = fields.Integer()
    facilities = fields.Many2many('room.facilities', string="Facilities")
    rent = fields.Float()

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
