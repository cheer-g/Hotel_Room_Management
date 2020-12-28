# -*- coding: utf-8 -*-
{
    'name': "Hotel Room Management",

    'summary': """
        Manage rooms and record accommodations for a Hotel""",

    'description': """
        This Hotel Room Management can record accommodation details 
    """,

    'author': "Sreerag E",
    'website': "http://cheer-g.github.io",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/accommodation.xml',
        'views/views.xml',
        'views/facility.xml',
        'views/templates.xml',
        'data/sequence.xml'
    ],
    # only loaded in demonstration mode
}
