from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import odoo.http as http


class PayrollPortal(CustomerPortal):
    @http.route("/payroll_generate", type="http", auth="public", website=True)
    def sample_portal_page(self, **kw):
        return http.request.render(
            "Refund.payroll_generate"
        )
