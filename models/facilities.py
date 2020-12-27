# -*- coding: utf-8 -*-

from random import randint
from odoo import models, fields


class RoomFacilities(models.Model):
    _name = 'room_management.facilities'
    _description = 'Room facilities'
    _rec_name = 'facility_name'

    facility_name = fields.Char(string="Facility Name", required=True)
    room_no = fields.Many2many('room.management')
