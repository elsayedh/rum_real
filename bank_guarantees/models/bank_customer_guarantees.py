# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError

class BankCustomerGuarantees(models.Model):
    _name = 'bank.customer.guarantees'
    _description = 'Bank Customer Guarandtees'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Guarantees Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))

    state = fields.Selection([('draft', 'Draft'),
                              ('approved', 'Approved'),
                              ('paid', 'Paid'),
                              ('renew', 'Renew'),
                              ('end', 'End'),
                              ('refund', 'Refund')], default='draft')

    guarantee_no = fields.Char(string="Guarantee Number")
    description = fields.Char(string="Description")
    customer_id = fields.Many2one('res.partner', string="Customer")  # 03 #domain for customers or verndors

    issue_date = fields.Date(string="Issue Date", required=True, default=lambda self: datetime.now())
    end_date = fields.Date(string="End Date")
    renew_date = fields.Date(string="Renew Date")

    guarantee_period = fields.Char(string="Guarantees Period")

    guarantee_amount = fields.Float(string="Guarantee Amount")  # 04 #currency field
    guarantee_type = fields.Selection([('basic_g', 'Basic Guarantee 1%'), ('final_g', 'Final Guarantee 5%')],
                                      string="Guarantees Type")

    guarantee_rate = fields.Char(string="Guarantee Rate")  # 05 #percentage %
    guarantee_total_amount = fields.Float(string="Guarantee Total Amount")  # 06 #currency field
    guarantee_expense = fields.Float(string="Guarantee Expense")  # 07 #currency field

    currency_id = fields.Many2one('res.currency')
    guarantee_total_other_c = fields.Float(string="Guarantee Total Amount (Other Currency)")  # 06 #other currency field

    vat = fields.Many2one('account.tax', string="VAT", domain=[('type_tax_use', '=', 'purchase')], required=True)

    bank_name = fields.Many2one('account.journal', domain=[('type', '=', 'bank')],
                                required=True)  # domain journal type = bank
    guarantee_expense_account = fields.Many2one('account.account', required=True)  # from chart of accounts
    guarantee_account = fields.Many2one('account.account', required=True)  # from chart of accounts
    notes = fields.Text(string="Notes")

    acc_refund_c = fields.Many2many('account.move.line', 'account_acc_refund_c', 'account_idx', 'acc_refund_c_id',
                                  string='Refunded Account')
    acc_move_paid = fields.Many2one('account.move', string="Journal Entries (Paid)", readonly=True)
    acc_move_renew = fields.Many2one('account.move', string="Journal Entries (Renew)", readonly=True)
    acc_move_refund = fields.Many2one('account.move', string="Journal Entries (Refund)", readonly=True)
    acc_paid = fields.Many2many('account.move.line')
    acc_renew_c = fields.Many2many('account.move.line', 'account_acc_renew_c', 'account_idx', 'acc_renew_c_id',
                                 string='Renewed Account')


    @api.onchange('guarantee_type', 'guarantee_amount')
    def guarantee_rating(self):
        if self.guarantee_type or self.guarantee_amount:
            if self.guarantee_type == 'basic_g':
                self.guarantee_rate = '1%'
                self.guarantee_total_amount = self.guarantee_amount * .01
            if self.guarantee_type == 'final_g':
                self.guarantee_rate = '5%'
                self.guarantee_total_amount = self.guarantee_amount * .05

    # Sending Email
    @api.model
    def mail_reminder(self):
        """Sending document expiry notification to employees."""

        now = datetime.now() + timedelta(days=1)
        print(now)
        date_now = now.date()
        match = self.search([])
        recipient_partners = []
        groups = self.env['res.groups'].search([('name', '=', 'Flags Barcode MANAGER')])
        print(groups)
        print('asd')
        for group in groups:
            print('asd1')
            for recipient in group.users:
                if recipient.partner_id.id not in recipient_partners:
                    recipient_partners.append(recipient.partner_id.id)

        actv_id = self.sudo().activity_schedule(
            'mail.mail_activity_data_todo', date_now,
            note=_(
                '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for <a href="#" data-oe-model="%s" data-oe-id="%s">%s\'s</a> Review') % (
                     self.name, self.name, self.name,
                     self.name, self.name),
            user_id=self.customer_id.email,
            res_id=self.id,

            summary=_("Request Approve")
        )
        print("active", actv_id)

        for i in match:
            if i.end_date:
                exp_date = fields.Date.from_string(i.end_date)
                if date_now == exp_date and i.state == 'paid':
                    mail_content2 = "Hello  " + str(i.customer_id.name) + ",<br>Your Bank Guarantees " \
                                    + str(i.name) + " is expired Today Please renew it. "

                    if len(recipient_partners):
                        i.message_post(body=mail_content2,
                                       subtype='mt_comment',
                                       subject=_('Bank Guarantees-%s Expired On %s') % (i.name, i.end_date),
                                       partner_ids=recipient_partners,
                                       message_type='comment')
        for i in match:
            if i.renew_date:
                exp_date2 = fields.Date.from_string(i.renew_date)
                if date_now == exp_date2 and i.state == 'paid':
                    mail_content2 = "Hello  " + str(i.customer_id.name) + ",<br>Your Bank Guarantees " \
                                    + str(i.name) + " is expired Today Please renew it. "

                    if len(recipient_partners):
                        i.message_post(body=mail_content2,
                                       subtype='mt_comment',
                                       subject=_('Bank Guarantees-%s Expired On %s') % (i.name, i.end_date),
                                       partner_ids=recipient_partners,
                                       message_type='comment')

    #######################
    #######################
    #######################

    # Sending Activity
    def make_activity(self):

        user_Obj = self.env['res.users'].browse(self.env.user.id)
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])

        for i in match:
            if i.end_date:
                print('test1')
                exp_date = fields.Date.from_string(i.end_date)
                if date_now == exp_date and i.state == 'paid':
                    print('test2')
                    act_type_xmlid = 'mail.mail_activity_data_todo'
                    print(act_type_xmlid)
                    date_deadline = datetime.now().strftime('%Y-%m-%d')
                    summary = ('Bank Guarantees-%s Expired') % (i.name)
                    note = "Hello  " + str(i.customer_id.name) + ",<br>Your Bank Guarantees " \
                           + str(i.name) + " is expired Today Please renew it. "

                    if act_type_xmlid:
                        print('test3')
                        activity_type = self.sudo().env.ref(act_type_xmlid)

                    model_id = self.env['ir.model']._get(self._name).id
                    print(model_id)
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary or activity_type.summary,
                        'automated': True,
                        'note': note,
                        'date_deadline': date_deadline,
                        'res_model_id': model_id,
                        'res_id': self.id,
                        'user_id': user_Obj.id,
                    }
                    print(create_vals)
                    self.env['mail.activity'].create(create_vals)

        for i in match:
            if i.renew_date:
                print('test1')
                exp_date = fields.Date.from_string(i.renew_date)
                if date_now == exp_date and i.state == 'paid':
                    print('test2')
                    act_type_xmlid = 'mail.mail_activity_data_todo'
                    print(act_type_xmlid)
                    date_deadline = datetime.now().strftime('%Y-%m-%d')
                    summary = ('Bank Guarantees-%s Expired') % (i.name)
                    note = "Hello  " + str(i.customer_id.name) + ",<br>Your Bank Guarantees " \
                           + str(i.name) + " is expired Today Please renew it. "

                    if act_type_xmlid:
                        print('test3')
                        activity_type = self.sudo().env.ref(act_type_xmlid)

                    model_id = self.env['ir.model']._get(self._name).id
                    print(model_id)
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary or activity_type.summary,
                        'automated': True,
                        'note': note,
                        'date_deadline': date_deadline,
                        'res_model_id': model_id,
                        'res_id': self.id,
                        'user_id': user_Obj.id,
                    }
                    print(create_vals)
                    self.env['mail.activity'].create(create_vals)

    ###############################
    ###############################
    ###############################

    def button_confirm(self):
        print(self.env.user.lang)
        return self.write({'state': 'approved'})

    def button_paid(self):
        account_id = self.env['account.move']

        total_vat = self.vat.amount / 100 * round(float(self.guarantee_expense), 2)
        total_after = round(float(self.guarantee_expense), 2) + round(float(total_vat), 2)

        acc_move_ids = account_id.create({
            'related_guarantee33': self.id,
            'date': self.issue_date,
            'journal_id': self.bank_name.id,
            'ref': str('PAID ' + self.name),
            'line_ids': [
                (0, 0, {
                    'account_id': self.bank_name.default_credit_account_id.id,
                    'name': str(self.bank_name.name) + " [" + str(self.customer_id.name) + "]",
                    'credit': self.guarantee_total_amount
                }),
                (0, 0, {
                    'account_id': self.bank_name.default_credit_account_id.id,
                    'name': 'Letter of guarantee expense',
                    'credit': total_after
                }),
                (0, 0, {
                    'account_id': self.vat.invoice_repartition_line_ids.account_id.id,
                    'name': "VAT " + str(self.vat.type_tax_use).capitalize() + " " + str(self.vat.name),
                    'debit': total_vat
                }),
                (0, 0, {
                    'account_id': self.guarantee_expense_account.id,
                    'tax_ids': self.vat,
                    'debit': self.guarantee_expense
                }),
                (0, 0, {
                    'account_id': self.guarantee_account.id,
                    'name': str(self.guarantee_no) + " " + str(self.description),
                    'debit': self.guarantee_total_amount
                }),
            ]
        })
        self.acc_move_paid = acc_move_ids
        self.acc_paid = acc_move_ids.line_ids
        return self.write({'state': 'paid'})

    def button_renew_end(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bank.customer.guarantees.wizard',
            'target': 'new',
        }

    def button_refund(self):
        account_id = self.env['account.move']
        acc_move_ids = account_id.create({
            'related_guarantee33': self.id,
            'date': self.issue_date,
            'journal_id': self.bank_name.id,
            'ref': str('REFUND ' + self.name),
            'line_ids': [
                (0, 0, {
                    'account_id': self.bank_name.default_credit_account_id.id,
                    'name': str(self.bank_name.name) + " [" + str(self.customer_id.name) + "]",
                    'debit': self.guarantee_expense
                }),

                (0, 0, {
                    'account_id': self.guarantee_account.id,
                    'name': str(self.name) + " " + str(self.description),
                    'credit': self.guarantee_expense
                }),
            ]
        })
        self.acc_move_refund = acc_move_ids
        self.acc_refund_c = acc_move_ids.line_ids
        return self.write({'state': 'refund'})

    def button_set_draft(self):
        return self.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        print('test')
        # assigning the sequence for the record
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('bank.customer.guarantees') or _('New')
        res = super(BankCustomerGuarantees, self).create(vals)
        return res

    @api.onchange('issue_date', 'end_date')
    def _computed_period(self):

        if self.issue_date and self.end_date:
            fmt = '%Y-%m-%d'
            frst_date = str(self.issue_date)
            scnd_date = str(self.end_date)
            d1 = datetime.strptime(frst_date, fmt)
            d2 = datetime.strptime(scnd_date, fmt)
            total_period = (d2 - d1).days

            if self.env.user.lang == 'ar_001':
                total_period = str(total_period) + str(" يوم")
                self.guarantee_period = total_period
            else:
                if total_period > 1 or total_period == 0:
                    total_period = str(total_period) + str(" Days")
                    self.guarantee_period = total_period
                elif total_period == 1:
                    total_period = str(total_period) + str(" Day")
                    self.guarantee_period = total_period

    def _bg_invoice_amount(self):
        for each in self:
            invoice_amount_ids = self.env['account.move'].sudo().search([('guarantee_letter33', '=', each.id)])
            if invoice_amount_ids:
                for i in invoice_amount_ids:
                    each.bg_invoice_amount += i.amount_total_signed
            else:
                each.bg_invoice_amount = 0

    def bg_invoice_view(self):
        self.ensure_one()
        domain = [
            ('guarantee_letter33', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                               Click to Create for New Record
                            </p>'''),
            'limit': 80,
            'context': "{'default_guarantee_letter33': '%s'}" % self.id
        }

    bg_invoice_amount = fields.Integer(compute="_bg_invoice_amount")


class BankCustomerGuaranteesWizard(models.Model):
    _name = 'bank.customer.guarantees.wizard'

    renew = fields.Boolean('Renew ?')
    new_end_date = fields.Date('New EndDate')

    def end_state(self):
        record_id = self.env['bank.customer.guarantees'].search([('id', '=', self.env.context.get('active_id'))])

        account_id = record_id.env['account.move']
        acc_move_ids = account_id.create({
            'related_guarantee33': record_id.id,
            'date': record_id.issue_date,
            'journal_id': record_id.bank_name.id,
            'ref': str('REFUND ' + record_id.name),
            'line_ids': [
                (0, 0, {
                    'account_id': record_id.bank_name.default_credit_account_id.id,
                    'name': str(record_id.bank_name.name) + " [" + str(record_id.customer_id.name) + "]",
                    'debit': record_id.guarantee_expense
                }),

                (0, 0, {
                    'account_id': record_id.guarantee_account.id,
                    'name': str(record_id.name) + " " + str(record_id.description),
                    'credit': record_id.guarantee_expense
                }),
            ]
        })
        record_id.acc_move_refund = acc_move_ids
        record_id.acc_refund_c = acc_move_ids.line_ids
        record_id.write({'state': 'refund'})

    def renew_state(self):
        record_id = self.env['bank.customer.guarantees'].search([('id', '=', self.env.context.get('active_id'))])
        record_id.end_date = self.new_end_date

        if not self.new_end_date:
            raise ValidationError(_("Please Enter New 'End Date' Field"))

        fmt = '%Y-%m-%d'
        frst_date = str(record_id.issue_date)
        scnd_date = str(record_id.end_date)
        d1 = datetime.strptime(frst_date, fmt)
        d2 = datetime.strptime(scnd_date, fmt)
        total_period = (d2 - d1).days

        if self.env.user.lang == 'ar_001':
            total_period = str(total_period) + str(" يوم")
            record_id.guarantee_period = total_period
        else:
            if total_period > 1 or total_period == 0:
                total_period = str(total_period) + str(" Days")
                record_id.guarantee_period = total_period
            elif total_period == 1:
                total_period = str(total_period) + str(" Day")
                record_id.guarantee_period = total_period

        account_id = record_id.env['account.move']
        total_vat = record_id.vat.amount / 100 * round(float(record_id.guarantee_expense), 2)
        total_expense_after = round(float(total_vat), 2) + round(float(record_id.guarantee_expense), 2)

        acc_move_ids = account_id.create({
            'related_guarantee33': record_id.id,
            'date': record_id.issue_date,
            'journal_id': record_id.bank_name.id,
            'ref': str('PAID ' + record_id.name),
            'line_ids': [
                (0, 0, {
                    'account_id': record_id.bank_name.default_credit_account_id.id,
                    'name': str(record_id.bank_name.name) + " [" + str(record_id.customer_id.name) + "]",
                    'credit': total_expense_after,
                }),
                (0, 0, {
                    'account_id': record_id.vat.invoice_repartition_line_ids.account_id.id,
                    'name': "VAT " + str(record_id.vat.type_tax_use).capitalize() + " " + str(record_id.vat.name),
                    'debit': total_vat
                }),
                (0, 0, {
                    'account_id': record_id.guarantee_account.id,
                    'name': str(record_id.guarantee_no) + " " + str(record_id.description),
                    'debit': record_id.guarantee_expense
                }),
            ]
        })
        record_id.acc_move_renew = acc_move_ids
        record_id.acc_renew_c = acc_move_ids.line_ids
        record_id.write({'state': 'end'})


class AccMoveInheriting33(models.Model):
    _inherit = 'account.move'

    related_guarantee33 = fields.Many2one('bank.customer.guarantees', string="Customer Guarantee", help="Related Customer Guarantee Letter", readonly=True)

    is_guarantee_letter33 = fields.Boolean('Is Guarantee Letter', help="Customer Guarantee Letter")
    guarantee_letter33 = fields.Many2one('bank.customer.guarantees', string="Generated Letter", domain=[('guarantee_type', '=', 'final_g')], help="Customer Guarantee Letter")