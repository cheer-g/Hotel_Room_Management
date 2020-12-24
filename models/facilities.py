# -*- coding: utf-8 -*-


from odoo import models, fields


class Facilities(models.Model):
    _name = 'room.facilities'
    _description = 'room_facilities'

    facility = fields.Char()
