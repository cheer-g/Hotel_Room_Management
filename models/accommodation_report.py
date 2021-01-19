# -*- coding: utf-8 -*-

from odoo import models, api, fields


class AccommodationReport(models.Model):
    _name = 'report.room_management.accommodation'

    date_from = fields.Date()
    date_to = fields.Date()
    guest_id = fields.Many2one('res.partner')

    def action_print_pdf(self):
        """print pdf action"""
        print("Guest : ", self.guest_id.name)
        data = {
            'model_id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id.id
        }
        return self.env.ref('room_management.report_hotel_accommodation'
                            ).report_action(self, data=data)

    @api.model
    def _get_report_values(self, docids, data):
        """Access the data returned from the button"""
        model_id = data['model_id']
        value = []
        guest = data['guest_id']
        print("Test Out : ", guest)
        if guest:
            query = """ SELECT guest_id, check_in, check_out, room_no_id, 
                        partner.name, rent_amount
                        FROM room_accommodation as room
                        INNER JOIN res_partner as partner
                        ON room.guest_id = partner.id
                        WHERE room.guest_id = %s""" % guest
        else:
            query = """ SELECT guest_id, check_in, check_out, room_no_id, 
                        rent_amount, partner.name
                        FROM room_accommodation as room
                        INNER JOIN res_partner as partner
                        ON room.guest_id = partner.id"""
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        print("Record : ", record)
        return {
            'docs': record,
            'date_today': fields.Datetime.now()
        }
