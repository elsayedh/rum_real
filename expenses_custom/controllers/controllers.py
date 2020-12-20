# -*- coding: utf-8 -*-
# from odoo import http


# class ExpensesCustom(http.Controller):
#     @http.route('/expenses_custom/expenses_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expenses_custom/expenses_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expenses_custom.listing', {
#             'root': '/expenses_custom/expenses_custom',
#             'objects': http.request.env['expenses_custom.expenses_custom'].search([]),
#         })

#     @http.route('/expenses_custom/expenses_custom/objects/<model("expenses_custom.expenses_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expenses_custom.object', {
#             'object': obj
#         })
