# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rum_product_report(models.Model):
#     _name = 'rum_product_report.rum_product_report'
#     _description = 'rum_product_report.rum_product_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
