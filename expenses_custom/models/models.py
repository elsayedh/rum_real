# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class ExpensesStatus(models.Model):
    _inherit = 'hr.expense.sheet'

    is_maximum = fields.Boolean(default=False)

    def action_sheet_move_create(self):
        print(self.is_maximum)
        print(self.total_amount)
        res_conf = self.env['res.config.settings'].sudo()
        max_amount = res_conf.get_values()
        print(max_amount['maximum_amount_approver'])
        if self.env.user.has_group('hr_expense.group_hr_expense_manager') or self.total_amount < max_amount['maximum_amount_approver']:
            if any(sheet.state != 'approve' for sheet in self):
                raise UserError(_("You can only generate accounting entry for approved expense(s)."))
            print('1working')
            if any(not sheet.journal_id for sheet in self):
                raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))

            expense_line_ids = self.mapped('expense_line_ids')\
                .filtered(lambda r: not float_is_zero(r.total_amount, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
            res = expense_line_ids.action_move_create()

            if not self.accounting_date:
                self.accounting_date = self.account_move_id.date

            if self.payment_mode == 'own_account' and expense_line_ids:
                self.write({'state': 'post'})
            else:
                self.write({'state': 'done'})
            self.activity_update()

            if self.total_amount < max_amount['maximum_amount_approver']:
                self.is_maximum = False
            elif self.total_amount > max_amount['maximum_amount_approver']:
                self.is_maximum = True
            print(self.is_maximum)

            return res

        else:

            if self.total_amount > max_amount['maximum_amount_approver']:
                print(self.is_maximum)
                self.is_maximum = True
            print('3working')
            print(self.is_maximum)
            raise UserError(_("Sorry, You have no permission to do this action."))

    # @api.depends('expense_line_ids.total_amount_company')
    # def _compute_amount(self):
    #     for sheet in self:
    #         sheet.total_amount = sum(sheet.expense_line_ids.mapped('total_amount_company'))
    #
    #     res_conf = self.env['res.config.settings'].sudo()
    #     max_amount = res_conf.get_values()
    #     if self.total_amount > max_amount['maximum_amount_approver']:
    #         self.is_maximum = True
    #     elif self.total_amount < max_amount['maximum_amount_approver']:
    #         self.is_maximum = False
    #
    #     print(max_amount['maximum_amount_approver'])
    #     print(self.total_amount)


    # @api.onchange('total_amount')
    # def product_amount_maximum(self):
    #     if self.expense_line_ids.product_id:
    #         print('Successfully')
    #         print('z')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    maximum_amount_approver = fields.Float(string="Approver Maximum Amount", help="This field contains an value to set a maximum amount for the 'team approver' and 'all approver' to post a journal in the expenses records")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config = self.env['ir.config_parameter'].sudo()
        am_approver=float(config.get_param('maximum_amount_approver'))
        res.update(
            maximum_amount_approver=am_approver,
        )
        return res

    def set_values(self):
        res=super(ResConfigSettings, self).set_values()
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('maximum_amount_approver',self.maximum_amount_approver)
        return res
