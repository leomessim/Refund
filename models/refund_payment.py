from odoo import models, fields, api
from odoo.exceptions import UserError


class RefundPayment(models.Model):
    _name = 'refund.payment'
    _inherit = 'mail.thread'
    _description = 'Refund Payment'

    name = fields.Char(string='Name', readonly=True)
    amount = fields.Float(string='Total Refund', readonly=True)
    batch = fields.Char(string='Batch', readonly=True)
    course = fields.Many2one('logic.courses', string='Course', readonly=True)
    id_refund_record = fields.Integer(string='Refund Record id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    status = fields.Selection([
        ('in_payment', 'Draft'),
        ('cancel', 'Cancel'),
        ('paid', 'Paid'),
    ], string='Status', default='in_payment')
    transaction_id = fields.Char(string='Transaction Id')
    student_admission_no = fields.Char('Admission Number', readonly=True)
    # invoice_number = fields.Char('Invoice number', readonly=True)
    # invoice_date = fields.Date('Invoice date', readonly=True)
    date_of_refund = fields.Date('Refund Date')
    refund_amount = fields.Float('Amount Refunded', help="Please enter the refund amount here: ", required=True)
    account_number = fields.Char(string='Account Number')
    account_holder_name = fields.Char(string='Account holder name')
    ifsc_code = fields.Char(string='IFSC Code')
    bank_name = fields.Char(string='Bank Name')

    # @api.depends('refund_amount')
    # def refund_amound_total(self):
    #     for rec in self:
    #         rec.total_refund = self.refund_amount

    total_refund = fields.Float('Total Amount')

    def paid(self):
        ss = self.env['student.refund'].search([])
        for i in ss:
            if self.name == i.student_name and self.student_admission_no == i.student_admission_no and self.id_refund_record == i.id:
                i.status = 'paid'
        self.status = 'paid'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Paid successfully.',
                'type': 'rainbow_man',
            }
        }

    def cancel(self):
        self.status = 'cancel'

    def compute_count(self):
        for record in self:
            record.form_count = self.env['student.refund'].search_count(
                [('id', '=', self.id_refund_record)])

    form_count = fields.Integer(compute='compute_count')

    def get_payments_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Refund',
            'view_mode': 'tree,form',
            'res_model': 'student.refund',
            'domain': [('id', '=', self.id_refund_record)],
            'context': "{'create': False}"
        }
