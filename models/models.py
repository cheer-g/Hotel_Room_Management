# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RoomManagement(models.Model):
    _name = 'room.management'
    _description = 'room_management'
    _rec_name = 'room_no'

    def _compute_accommodation_count(self):
        for rec in self:
            lists = self.env['room.accommodation'].search([
                ('room_no_id', '=', rec.room_no)])
            rec.accommodation_count = len(lists)


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
    accommodations_id = fields.Many2one('room.accommodation',
                                        domain=[('room_no_id', '=', room_no)])
    accommodation_count = fields.Integer(compute=_compute_accommodation_count)

    _sql_constraints = [
        ('Room_no', 'unique (room_no)', 'This Room No. Already exist!')]

    def get_accommodation(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accommodations',
            'view_mode': 'tree,form',
            'res_model': 'room.accommodation',
            'domain': [('room_no_id', '=', self.room_no)],
            'context': "{'create': False}"
        }