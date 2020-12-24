# -*- coding: utf-8 -*-
from odoo import http


class RoomManagement(http.Controller):
    @http.route('/room_management/room_management/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/room_management/room_management/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('room_management.listing', {
            'root': '/room_management/room_management',
            'objects': http.request.env['room_management.room_management'].search([]),
        })

    @http.route('/room_management/room_management/objects/<model("room_management.room_management"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('room_management.object', {
            'object': obj
        })
