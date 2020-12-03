from odoo import models, fields, api


class GuaranteeCustomerReportWizard(models.TransientModel):
    _name = 'guarantee.customer.report.wizard'


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", default=fields.Date.today)
    guarantee_type = fields.Selection([('basic_g','Basic Guarantee 1%'),('final_g','Final Guarantee 5%')],
                                         string="Guarantees Type")
    print_all = fields.Boolean()
    state = fields.Selection([('draft','Draft'),
                              ('approved','Approved'),
                              ('paid','Paid'),
                              ('renew','Renew'),
                              ('end','End'),
                              ('refund','Refund')])


    def get_guarantee_customer_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'print_all': self.print_all,
                'state': self.state,
                'guarantee_type': self.guarantee_type,
            },
        }
        return self.env.ref('bank_guarantees.guarantee_customer_report_report').report_action(self, data=data)


class GuaranteeCustomerReportReportView(models.AbstractModel):
    _name = "report.bank_guarantees.guarantee_customer_report_report_view"
    _description = "Guarantee Customer Report"

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = []


        domains = []
        if data['form']['start_date']:
            domains.append(('issue_date', '>=', data['form']['start_date']))
            domains.append(('issue_date', '<=', data['form']['end_date']))
        if data['form']['state']:
            domains.append(('state', '=', data['form']['state']))
        if data['form']['guarantee_type']:
            domains.append(('guarantee_type', '=', data['form']['guarantee_type']))

        customers = self.env['bank.customer.guarantees'].search(domains, order='name asc')

        if data['form']['print_all']:
            customers = self.env['bank.customer.guarantees'].search([], order='name asc')

        # if data['form']['start_date'] and data['form']['state'] and data['form']['guarantee_type']:
        #     customers = self.env['bank.customer.guarantees'].search([('guarantee_type', '=', data['form']['guarantee_type']),
        #                                                 ('state', '>=', data['form']['state']),
        #                                                 ('issue_date', '>=', data['form']['start_date']),
        #                                                 ('issue_date', '<=', data['form']['end_date'])
        #                                                 ], order='name asc')
        #
        # if data['form']['start_date'] and data['form']['guarantee_type']:
        #     customers = self.env['bank.customer.guarantees'].search([('guarantee_type', '=', data['form']['guarantee_type']),
        #                                                          ('issue_date', '>=', data['form']['start_date']),
        #                                                          ('issue_date', '<=', data['form']['end_date'])
        #                                                          ], order='name asc')
        # if data['form']['start_date'] and data['form']['state']:
        #     customers = self.env['bank.customer.guarantees'].search([('state', '=', data['form']['state']),
        #                                                          ('issue_date', '>=', data['form']['start_date']),
        #                                                          ('issue_date', '<=', data['form']['end_date'])
        #                                                          ], order='name asc')
        #
        # if data['form']['start_date'] and data['form']['start_date']:
        #     customers = self.env['bank.customer.guarantees'].search([('issue_date', '>=', data['form']['start_date']),
        #                                                          ('issue_date', '<=', data['form']['end_date'])
        #                                                          ], order='name asc')
        #
        # if data['form']['state']:
        #     customers = self.env['bank.customer.guarantees'].search([('state', '=', data['form']['state'])
        #                                                 ], order='name asc')
        #
        # if data['form']['guarantee_type']:
        #     customers = self.env['bank.customer.guarantees'].search([('guarantee_type', '=', data['form']['guarantee_type'])
        #                                                 ], order='name asc')
        #
        # if data['form']['guarantee_type'] and data['form']['state']:
        #     customers = self.env['bank.customer.guarantees'].search([('guarantee_type', '=', data['form']['guarantee_type']),
        #                                                          ('state', '=', data['form']['state'])], order='name asc')

        for customer in customers:
            guarantee_type = dict(customer._fields['guarantee_type'].selection).get(customer.guarantee_type)
            state = dict(customer._fields['state'].selection).get(customer.state)
            docs.append({
                'start_date': data['form']['start_date'],
                'end_date': data['form']['end_date'],
                'description': customer.description,
                'bank_name': customer.bank_name.name,
                'customer_id': customer.customer_id.name,
                'guarantee_type': guarantee_type,
                'state': state,
                'guarantee_expense': customer.guarantee_expense,
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': data['form']['start_date'],
            'date_end': data['form']['end_date'],
            'state': data['form']['state'],
            'docs': docs,
        }
