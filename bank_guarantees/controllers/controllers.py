# -*- coding: utf-8 -*-
# from odoo import http


# class BankGuarantees(http.Controller):
#     @http.route('/bank_guarantees/bank_guarantees/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bank_guarantees/bank_guarantees/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bank_guarantees.listing', {
#             'root': '/bank_guarantees/bank_guarantees',
#             'objects': http.request.env['bank_guarantees.bank_guarantees'].search([]),
#         })

#     @http.route('/bank_guarantees/bank_guarantees/objects/<model("bank_guarantees.bank_guarantees"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bank_guarantees.object', {
#             'object': obj
#         })
