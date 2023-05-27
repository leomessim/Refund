from odoo import fields, models, api, _
import requests
from datetime import date, datetime
from odoo.exceptions import UserError


class StudentRefund(models.Model):
    _name = 'student.refund'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference_no'
    _description = "Refund"

    student_name = fields.Char(string='Name', readonly=True)
    reference_no = fields.Char(string="Sequence Number", readonly=True, required=True,
                               copy=False, default='New')

    amount = fields.Float(string='Amount', readonly=True)
    batch = fields.Char(string='Batch', readonly=True)
    course = fields.Char(string='Course', readonly=True)
    email = fields.Char(string='Email', readonly=True)
    phone_number = fields.Char(string='Phone number', widget='phone', readonly=True)
    reason = fields.Text(string='Student reason', readonly=True)
    status = fields.Selection([
        ('accountant', 'Draft'),
        ('teacher', 'Teacher Approval'),
        ('head', 'Head Approval'),
        ('manager', 'Manager Approval'),
        ('accounts', 'Approved'),
        ('reject', 'Rejected'),
        ('paid', 'Paid'),
    ], string='Status', default='accountant')

    branch = fields.Char('Branch', readonly=True)
    student_admission_no = fields.Char('Admission number', readonly=True)
    parent_number = fields.Char('Parent number', readonly=True)
    invoice_number = fields.Char('Invoice number', readonly=True)
    invoice_date = fields.Date('Invoice date', readonly=True)
    sat_class = fields.Integer(string='How many days he sat in the class')
    teacher_reason = fields.Text('Reason for teacher')
    head_reason = fields.Text('Reason for head')
    assign_to = fields.Many2one('res.users', string='Assign to')

    make_visible_teacher = fields.Boolean(string="User", default=True, compute='get_teacher')
    action_testing = fields.Float('Action')

    # def activity_schedule(self, act_type_xmlid='', date_deadline=None, summary='', note='', **act_values):
    #     """ Schedule an activity on each record of the current record set.
    #     This method allow to provide as parameter act_type_xmlid. This is an
    #     xml_id of activity type instead of directly giving an activity_type_id.
    #     It is useful to avoid having various "env.ref" in the code and allow
    #     to let the mixin handle access rights.
    #
    #     :param date_deadline: the day the activity must be scheduled on
    #     the timezone of the user must be considered to set the correct deadline
    #     """
    #     if self.env.context.get('mail_activity_automation_skip'):
    #         return False
    #
    #     if not date_deadline:
    #         date_deadline = fields.Date.context_today(self)
    #     if isinstance(date_deadline, datetime):
    #         _logger.warning("Scheduled deadline should be a date (got %s)", date_deadline)
    #     if act_type_xmlid:
    #         activity_type = self.env.ref(act_type_xmlid, raise_if_not_found=False) or self._default_activity_type()
    #     else:
    #         activity_type_id = act_values.get('activity_type_id', False)
    #         activity_type = activity_type_id and self.env['mail.activity.type'].sudo().browse(activity_type_id)
    #
    #     model_id = self.env['ir.model']._get(self._name).id
    #     activities = self.env['mail.activity']
    #     for record in self:
    #         create_vals = {
    #             'activity_type_id': activity_type and activity_type.id,
    #             'summary': summary or activity_type.summary,
    #             'automated': True,
    #             'note': note or activity_type.default_description,
    #             'date_deadline': date_deadline,
    #             'res_model_id': model_id,
    #             'res_id': record.id,
    #         }
    #         create_vals.update(act_values)
    #         if not create_vals.get('user_id'):
    #             create_vals['user_id'] = activity_type.default_user_id.id or self.env.uid
    #         activities |= self.env['mail.activity'].create(create_vals)
    #     return activities

    def confirm_assign(self):
        if not self.assign_to:
            raise UserError('Please assign a teacher..')
        else:
            self.status = 'teacher'
        # users = self.env.ref('refund_logic.group_refund_teacher').users
        # activity_type = self.env.ref('refund_logic.mail_activity_refund_alert_custome')
        # self.activity_schedule('refund_logic.mail_activity_refund_alert_custome', user_id=self.assign_to.id,
        #                        note=f'Please Approve {self.assign_to.name}')
        #
        # print(self.env.ref('refund_logic.mail_activity_refund_alert_custome').id, 'lll')

    @api.depends('make_visible_teacher')
    def get_teacher(self):
        print('kkkll')
        user_crnt = self.env.user.id

        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('Refund.group_refund_teacher'):
            self.make_visible_teacher = False

        else:
            self.make_visible_teacher = True

    make_visible_head = fields.Boolean(string="User", default=True, compute='get_head')

    @api.depends('make_visible_head')
    def get_head(self):
        print('kkkll')
        user_crnt = self.env.user.id

        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('Refund.group_refund_marketing_head'):
            self.make_visible_head = False

        else:
            self.make_visible_head = True

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'student.refund') or _('New')
        res = super(StudentRefund, self).create(vals)
        return res

    # def accountant_approval(self):
    #     # self.make_visible_teacher = True
    #     self.status = 'teacher'

    def teacher_approval(self):
        self.message_post(body="Teacher is approved")
        self.status = 'head'
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        activity_id.action_feedback(feedback='Teacher Approved')
        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        other_activity_ids.unlink()
        # self.activity_schedule('refund_logic.mail_activity_refund_alert_custome', user_id=user.id,
        #                        note='Please Approve')

    def head_approval(self):
        self.message_post(body="Head is approved")
        self.status = 'manager'
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        activity_id.action_feedback(feedback='Head Approved')
        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        other_activity_ids.unlink()

    def manager_approval(self):
        self.message_post(body="Marketing Manager is approved")
        self.env['refund.payment'].create({
            'name': self.student_name,
            'amount': self.amount,
            'batch': self.batch,
            'course': self.course,
            'student_admission_no': self.student_admission_no,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,

        }
        )
        self.status = 'accounts'
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        activity_id.action_feedback(feedback='Manager Approved')
        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        other_activity_ids.unlink()

    def rejected(self):
        self.status = 'reject'
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        activity_id.action_feedback(feedback=f'Rejected {self.env.user.name}')
        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('Refund.mail_activity_refund_alert_custome').id)])
        other_activity_ids.unlink()

        # current = self.env.user
        # main_content = {
        #     'subject': 'STUDENT REFUND',
        #     'body_html': f"<h1>Hello {self.name} Your refund request is rejected..</h1>",
        #     'email_to': self.email,
        #     # 'attachment_ids': attachment
        #
        # }
        # self.env['mail.mail'].create(main_content).send()

    def paid_payments(self):
        self.status = 'paid'

    def teacher_refund_activity(self):
        print('hhhi')
        ss = self.env['student.refund'].search([])
        for i in ss:
            if i.status == 'teacher':
                users = ss.env.ref('Refund.group_refund_teacher').users
                activity_type = i.env.ref('Refund.mail_activity_refund_alert_custome')
                i.activity_schedule('Refund.mail_activity_refund_alert_custome', user_id=i.assign_to.id,
                                    note=f'Please Approve {i.assign_to.name}')

    def head_refund_activity(self):
        print('hhhi')
        ss = self.env['student.refund'].search([])
        for i in ss:
            if i.status == 'head':
                users = ss.env.ref('Refund.group_refund_marketing_head').users
                for j in users:
                    activity_type = i.env.ref('Refund.mail_activity_refund_alert_custome')
                    i.activity_schedule('Refund.mail_activity_refund_alert_custome', user_id=j.id,
                                        note=f'Please Approve {j.name}')

    def accounts_request_refund_activity(self):
        print('hhhi')
        ss = self.env['student.refund'].search([])
        for i in ss:
            if i.status == 'accountant':
                users = ss.env.ref('Refund.group_refund_accounts').users
                for j in users:
                    activity_type = i.env.ref('Refund.mail_activity_refund_alert_custome')
                    i.activity_schedule('Refund.mail_activity_refund_alert_custome', user_id=j.id,
                                        note='Received a new Refund request form')

    def marketing_refund_activity(self):
        print('hhhi')
        ss = self.env['student.refund'].search([])
        for i in ss:
            if i.status == 'manager':
                users = ss.env.ref('Refund.refund_manager').users
                for j in users:
                    activity_type = i.env.ref('Refund.mail_activity_refund_alert_custome')
                    i.activity_schedule('Refund.mail_activity_refund_alert_custome', user_id=j.id,
                                        note=f'Please Approve {j.name}')


class PaymentDetails(models.Model):
    _name = 'payment.details'
    _inherit = 'mail.thread'

    refund_amount = fields.Float(string='Refund amount')
    refund_date = fields.Date(string='Refund date')
    transaction_id = fields.Integer(string='Transaction id')
