# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo .exceptions import ValidationError


class AccommodationReport(models.Model):
    _name = 'report.room_management.accommodation'

    date_from = fields.Date()
    date_to = fields.Date()
    guest_id = fields.Many2one('res.partner')
    check_out = fields.Boolean()

    def action_print_pdf(self):
        """print pdf action"""
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValidationError("Date From must be less than Date To")

        data = {
            'model_id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id.id,
            'check_out': self.check_out
        }
        return self.env.ref('room_management.report_hotel_accommodation'
                            ).report_action(self, data=data)

    @api.model
    def _get_report_values(self, docids, data):
        """Access the data returned from the button"""
        model_id = data['model_id']
        value = []
        if data['guest_id']:
            guest = data['guest_id']
        else:
            guest = False

        check_out = data['check_out']
        date_from = data['date_from']
        date_to = data['date_to']
        # print("Test Out : ", type(date_from))

        if guest:
            if check_out:
                if date_from:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE room.guest_id = %s
                                    AND CAST(room.check_out AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    AND CAST(room.check_out AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % (guest, date_from, date_to)
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_out AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    AND room.guest_id = %s
                                    ORDER BY CAST(room.check_in AS DATE)""" % (date_from, guest)
                else:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE room.guest_id = %s
                                    AND CAST(room.check_out AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % (guest, date_to)
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE room.guest_id = %s
                                    AND CAST(room.check_out AS DATE) IS NOT NULL
                                    ORDER BY CAST(room.check_in AS DATE)""" % guest
            else:
                if date_from:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE room.guest_id = %s
                                    AND CAST(room.check_out AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    AND CAST(room.check_out AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % (guest, date_from, date_to)
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_in AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    AND room.guest_id = %s
                                    ORDER BY CAST(room.check_in AS DATE)""" % (date_from, guest)
                else:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE room.guest_id = %s
                                    AND CAST(room.check_in AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % (guest, date_to)
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE room.guest_id = %s
                                    ORDER BY CAST(room.check_in AS DATE)""" % guest
        else:
            if check_out:
                if date_from:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_out AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    AND CAST(room.check_out AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % (date_from, date_to)
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_out AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % date_from
                else:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_out AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % date_to
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    ORDER BY CAST(room.check_in AS DATE)"""
            else:
                if date_from:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_in AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    AND CAST(room.check_in AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % (date_from, date_to)
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_in AS DATE) >= 
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % date_from
                else:
                    if date_to:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, partner.name, rent_amount
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    WHERE CAST(room.check_in AS DATE) <=
                                    CAST('%s' AS DATE)
                                    ORDER BY CAST(room.check_in AS DATE)""" % date_to
                    else:
                        query = """ SELECT guest_id, check_in, check_out, 
                                    room_no.room_no, rent_amount, partner.name
                                    FROM room_accommodation as room
                                    INNER JOIN res_partner as partner
                                    ON room.guest_id = partner.id
                                    INNER JOIN room_management as room_no
                                    ON room.room_no_id = room_no.id
                                    ORDER BY CAST(room.check_in AS DATE)"""

        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        print("Record : ", record)
        guest_name = False
        for rec in record:
            guest_name = rec['name']
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
            'guest': guest,
            'guest_name': guest_name,
            'date_from': date_from,
            'date_to': date_to
        }
