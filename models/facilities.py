# -*- coding: utf-8 -*-

from random import randint
from odoo import models, fields


class RoomFacilities(models.Model):
    _name = 'room_management.facilities'
    _description = 'Room facilities'
    _rec_name = 'facility_name'

    # def _get_default_color(self):
    #     return randint(1, 11)

    facility_name = fields.Char(string="Facility Name", required=True)
    # color = fields.Integer(string='Color Index', default=_get_default_color)
    # facility_ids = fields.Many2many('room.management', string='Facilities')

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Facility already exists !"),
    # ]
