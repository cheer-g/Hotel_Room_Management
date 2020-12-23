# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HotelRooms(models.Model):
    _name = 'hotel_rooms.hotel_rooms'
    _description = 'hotel_rooms.hotel_rooms'

    room_no = fields.Integer()
    bed = fields.Selection(selection=[('single', 'Single'), ('double', 'Double'), ('dorm', 'Dormitory')])
    total_beds = fields.Integer()
    facilities = fields.Text()
    rent = fields.Float()
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
