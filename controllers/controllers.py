# -*- coding: utf-8 -*-
from odoo import http


class HotelRooms(http.Controller):
    @http.route('/hotel_rooms/hotel_rooms/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/hotel_rooms/hotel_rooms/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('hotel_rooms.listing', {
            'root': '/hotel_rooms/hotel_rooms',
            'objects': http.request.env['hotel_rooms.hotel_rooms'].search([]),
        })

    @http.route('/hotel_rooms/hotel_rooms/objects/<model("hotel_rooms.hotel_rooms"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('hotel_rooms.object', {
            'object': obj
        })
