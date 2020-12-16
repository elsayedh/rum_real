# -*- coding: utf-8 -*-
# from odoo import http


# class SecurityFlags(http.Controller):
#     @http.route('/security_flags/security_flags/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/security_flags/security_flags/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('security_flags.listing', {
#             'root': '/security_flags/security_flags',
#             'objects': http.request.env['security_flags.security_flags'].search([]),
#         })

#     @http.route('/security_flags/security_flags/objects/<model("security_flags.security_flags"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('security_flags.object', {
#             'object': obj
#         })
