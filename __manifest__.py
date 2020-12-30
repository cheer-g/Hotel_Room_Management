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

    'category': 'Tools',
    'version': '2.0',
    'depends': ['base', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/accommodation.xml',
        'views/views.xml',
        'views/facility.xml',
        'views/templates.xml',
        'data/sequence.xml'
    ],
}
