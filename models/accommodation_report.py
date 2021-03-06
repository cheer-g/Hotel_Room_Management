# -*- coding: utf-8 -*-

import json
import io
from odoo import models, api, fields
from odoo .exceptions import ValidationError
from odoo.tools import date_utils


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

    def print_xlsx(self):
        """XLSX Report print method"""
        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValidationError("Date From must be less than Date To")

        # active_record = self._context['id']
        # record = self.env['room.accommodation'].browse(active_record)
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id.id,
            'model_id': self.id,
            'check_out': self.check_out,
            'date_today': fields.Datetime.now()
        }

        print("XLSX Wizard data : ", data)

        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'accommodation.reporting',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': 'Accommodation Report'
            },
            'report_type': 'xlsx'
        }

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

        # Queries for different conditions
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

    def get_xlsx_report(self, data, response):
        """Report generation"""
        value = []
        user_obj = self.env.user
        model_id = data['model_id']
        check_out = data['check_out']
        date_from = data['date_from']
        date_to = data['date_to']
        today = data['date_today']
        guest = False
        if data['guest_id']:
            guest = data['guest_id']
        print("Guest ID", guest)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True,
                                    'font_size': '20px'})
        col_head = workbook.add_format({'align': 'left', 'bold': True,
                                        'font_size': '9px'})
        txt = workbook.add_format({'font_size': '9px',})
        txt_center = workbook.add_format({'font_size': '9px',
                                          'align': 'center'})
        date = workbook.add_format({'num_format': 'dd/mm/yy', 'font_size': '9px'})
        money = workbook.add_format({'num_format': '₹#,##0', 'font_size': '9px'})

        sheet.merge_range('A1:B1', user_obj.company_id.name, txt)
        sheet.merge_range('B9:H10', 'Hotel Management', head)
        sheet.write('B11', 'Date', col_head)
        sheet.merge_range('C11:F11', today, date)
        if date_from:
            sheet.write('B13', 'From', col_head)
            sheet.write('C13', data['date_from'], date)
        if date_to:
            sheet.write('E13', 'To', col_head)
            sheet.write('F13', data['date_to'], date)
        sheet.write('B15', 'SL No.', col_head)
        if not guest:
            sheet.merge_range('C15:D15', 'Name', col_head)
            sheet.write('E15', 'Room No.', col_head)
            sheet.write('F15', 'Check-In', col_head)
            sheet.write('G15', 'Check-out', col_head)
            sheet.write('H15', 'Rent', col_head)
        else:
            sheet.write('C15', 'Room No.', col_head)
            sheet.write('D15', 'Check-In', col_head)
            sheet.write('E15', 'Check-out', col_head)
            sheet.write('F15', 'Rent', col_head)

        # Queries based on different conditions
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % \
                                (guest, date_from, date_to)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % \
                                (date_from, guest)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % \
                                (guest, date_to)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % (
                        guest, date_from, date_to)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % (
                        date_from, guest)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % (
                        guest, date_to)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % (
                        date_from, date_to)
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
                                    ORDER BY CAST(room.check_in AS DATE)""" % (
                        date_from, date_to)
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
        guest_name = False
        for rec in record:
            guest_name = rec['name']
        if guest and guest_name:
            sheet.write('B12', 'Guest', col_head)
            sheet.merge_range('C12:F12', guest_name, txt)
        print("Record : ", record)
        row_no = 8
        col_no = 1
        i = 1
        if not record:
            sheet.merge_range('B9:F9', "No results", txt)
        for rec in record:
            sheet.write(row_no, col_no, i, txt_center)
            if not guest:
                sheet.merge_range(row_no, col_no + 1, row_no, col_no + 2,
                                  rec['name'], txt)
                sheet.write(row_no, col_no + 3, rec['room_no'], txt)
                sheet.write(row_no, col_no + 4, rec['check_in'], date)
                sheet.write(row_no, col_no + 5, rec['check_out'], date)
                sheet.write(row_no, col_no + 6, rec['rent_amount'], money)
            else:
                sheet.write(row_no, col_no + 1, rec['room_no'], txt)
                sheet.write(row_no, col_no + 2, rec['check_in'], date)
                sheet.write(row_no, col_no + 3, rec['check_out'], date)
                sheet.write(row_no, col_no + 4, rec['rent_amount'], money)
            row_no += 1
            i += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
