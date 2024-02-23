# -*- coding: utf-8 -*-
# from odoo import http


# class Quico(http.Controller):
#     @http.route('/quico/quico', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quico/quico/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('quico.listing', {
#             'root': '/quico/quico',
#             'objects': http.request.env['quico.quico'].search([]),
#         })

#     @http.route('/quico/quico/objects/<model("quico.quico"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quico.object', {
#             'object': obj
#         })
