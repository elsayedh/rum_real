from odoo import api, fields, models, _

class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.model
    def get_account_move_lines(self, domain=None):
        context = self._context or {}
        debit = 0.0
        credit = 0.0
        balance = 0.0
        domain = [('move_id.state', '=', 'posted')]
        for account in self:
            child_ids = self.env['account.account'].search([('id','child_of',[account.id])]).ids
            
            if child_ids:
                domain.append(('account_id','in',child_ids))
            if context['date_from'] != 'False':
                domain.append(('date', '>=', context['date_from']))               
            if context['date_to'] != 'False':
                domain.append(('date', '<=', context['date_to']))

            for line in self.env['account.move.line'].search(domain):
                balance += line.debit - line.credit
                credit += line.credit
                debit += line.debit
                
            account.balance = balance
            account.credit = credit
            account.debit = debit
        return debit, credit, balance
    


    @api.depends('account_move_line_ids','account_move_line_ids.amount_currency','account_move_line_ids.debit','account_move_line_ids.credit')
    def compute_account_values(self):
        for account in self:
            debit = 0.0
            credit = 0.0
            balance = 0.0
            child_ids = self.env['account.account'].search([('id','child_of',[account.id])]).ids
            for line in self.env['account.move.line'].search([('account_id','in',child_ids),('move_id.state', '=', 'posted')]):
                balance += line.debit - line.credit
                credit += line.credit
                debit += line.debit

            account.balance = balance
            account.credit = credit
            account.debit = debit

    parent_id = fields.Many2one('account.account', 'Parent Name')
    child_ids = fields.One2many('account.account', 'parent_id', 'Children')
    account_move_line_ids = fields.One2many('account.move.line', 'account_id', string='Move Lines', copy=False)
    balance = fields.Float(compute="compute_account_values",  string='Balance')
    credit = fields.Float(compute="compute_account_values", string='Credit')
    debit = fields.Float(compute="compute_account_values", string='Debit')
    has_child = fields.Boolean(string="Has Child", compute='_compute_has_child')
    
    @api.depends('child_ids')
    def _compute_has_child(self):
        for record in self:
            if len(record.child_ids) >= 1:
                record.has_child = True
            else:
                record.has_child = False
