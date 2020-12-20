# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    order_type1 = fields.Selection([('internal','Internal'),('external','External')], string="Order Type")
