# -*- coding: utf-8 -*-
# from odoo import http


# class RumProductReport(http.Controller):
#     @http.route('/rum_product_report/rum_product_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rum_product_report/rum_product_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rum_product_report.listing', {
#             'root': '/rum_product_report/rum_product_report',
#             'objects': http.request.env['rum_product_report.rum_product_report'].search([]),
#         })

#     @http.route('/rum_product_report/rum_product_report/objects/<model("rum_product_report.rum_product_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rum_product_report.object', {
#             'object': obj
#         })
