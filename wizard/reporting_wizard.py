# -*- coding: utf-8 -*-

import json
import io
from odoo import models, fields
from odoo .exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ExcelReportingWizard(models.TransientModel):
    _name = 'accommodation.reporting'

    date_from = fields.Date()
    date_to = fields.Date()
    guest_id = fields.Many2one('res.partner')

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
            'guest_id': self.guest_id,
            'model_id': self.id
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

    def get_xlsx_report(self, data, response):
        """Report generation"""
        print("get_xlsx test")
        value = []
        model_id = data['model_id']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True,
                                    'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        date = workbook.add_format({'num_format': 'dd/mm/yy'})

        sheet.merge_range('B2:I3', 'Accommodation Report', head)
        sheet.write('B6', 'From', cell_format)
        sheet.merge_range('C6:D6', data['date_from'], txt)
        sheet.write('F6', 'To', cell_format)
        sheet.merge_range('G6:H6', data['date_to'], txt)
        sheet.write('B8', 'SL No.', txt)
        sheet.write('C8', 'Name', txt)
        sheet.write('D8', 'Room No.', txt)
        sheet.write('E8', 'Check-In', txt)
        sheet.write('F8', 'Check-out', txt)
        sheet.write('G8', 'Rent', txt)
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
        row_no = 8
        col_no = 1
        i = 1
        for rec in record:
            sheet.write(row_no, col_no, i, txt)
            sheet.write(row_no, col_no+1, rec['name'], txt)
            sheet.write(row_no, col_no+2, rec['room_no'], txt)
            sheet.write(row_no, col_no+3, rec['check_in'], date)
            sheet.write(row_no, col_no+4, rec['check_out'], date)
            sheet.write(row_no, col_no+5, rec['rent_amount'], txt)
            row_no += 1
            i += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
