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

        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'guest_id': self.guest_id
        }

        return {
            'type': 'ir_actions_xlsx_download',
            'data': {
                'model': 'accommodation.reporting',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': 'Accommodation Report'
            }
        }

    def get_xlsx_report(self, data, response):
        """Report generation"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True,
                                    'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_rane('B2:I3', 'Accommodation Report', head)
        sheet.write('B6', 'From', cell_format)
        sheet.merge_range('C6:D6', data['date_from'], txt)
        sheet.write('F6', 'To', cell_format)
        sheet.merge_range('G6:H6', data['date_to'], txt)
        workbook.close()
        output.seek(0)
        response.strem.write(output.read())
        output.close()
