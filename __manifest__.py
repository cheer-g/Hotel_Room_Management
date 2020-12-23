# -*- coding: utf-8 -*-
{
    'name': "hotel_rooms",

    'summary': """
        Hotel Rooms Management""",

    'description': """
        User can create and manage hotel rooms
    """,

    'author': "Sreerag",
    'website': "http://cheer-g.github.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
