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
    'images': ['static/description/banner.png'],

    'category': 'Tools',
    'version': '14.0.2.1.2',
    'depends': ['base', 'contacts', 'uom', 'product', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/accommodation.xml',
        'views/views.xml',
        'views/facility.xml',
        'views/order_food_view.xml',
        'views/food_manage.xml',
        'views/templates.xml',
        'data/sequence.xml'
    ],
}
