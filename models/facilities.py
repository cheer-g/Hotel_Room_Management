# -*- coding: utf-8 -*-

from random import randint
from odoo import models, fields


class Facilities(models.Model):
    _name = 'room.facilities'
    _description = 'Room facilities'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Facility Name", required=True)
    color = fields.Integer(string='Color Index', default=_get_default_color)
    facility_ids = fields.Many2many('room.management', string='Facilities')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Facility already exists !"),
    ]
