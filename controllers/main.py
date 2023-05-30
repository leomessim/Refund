from odoo import http
from odoo.http import request


class PartnerForm(http.Controller):
    @http.route(['/refund/form'], type='http', auth="public", website=True, csrf=False)
    def partner_form(self, **kw):
        course = request.env['logic.courses'].search([])
        student_name = request.env['student.details'].sudo().search([])
        print(student_name)
        values = {
            'course': course,
            'student_name': student_name,
            # 'order': sale_order,
        }
        return request.render("Refund.tmp_refund_form", values)

    @http.route(['/refund/form/submit'], type='http', auth="public", website=True, csrf=False)
    def customer_form_submit(self, **kw):
        request.env['student.refund'].sudo().create({
            'student_name': kw.get('student_name'),
            'batch': kw.get('batch'),
            'course': kw.get('customer_id'),
            'amount': kw.get('amount'),
            'email': kw.get('email'),
            'phone_number': kw.get('phone'),
            'reason': kw.get('reason'),
            'branch': kw.get('branch'),
            'student_admission_no': kw.get('admission_no'),
            'parent_number': kw.get('parent_no'),
            'invoice_number': kw.get('invoice_no'),
            'invoice_date': kw.get('invoice_date')


            # 'sale_order_id': kw.get('sale_order')
        })

        # current = request.env['student.details'].sudo().search([])
        # for i in current:
        #     print('user', i.id)
        # main_content = {
        #     'subject': 'Student refund',
        #     'body_html': "Refund request",
        #     'email_to': request.email,
        #     # 'attachment_ids': attachment
        #
        # }
        # request.env['mail.mail'].create(main_content).send()
        return request.render("Refund.tmp_refund_form_success", {})
