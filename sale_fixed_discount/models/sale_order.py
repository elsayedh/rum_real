# Copyright 2017-20 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount_fixed = fields.Float(
        string="Discount (Fixed)",
        digits="Product Price",
        help="Fixed amount discount.",
    )

    @api.onchange("discount")
    def _onchange_discount_percent(self):
        # _onchange_discount method already exists in core,
        # but discount is not in the onchange definition
        if self.discount:
            self.discount_fixed = 0.0

    @api.onchange("discount_fixed")
    def _onchange_discount_fixed(self):
        if self.discount_fixed:
            self.discount = 0.0

    @api.constrains("discount", "discount_fixed")
    def _check_only_one_discount(self):
        for line in self:
            if line.discount and line.discount_fixed:
                raise ValidationError(
                    _("You can only set one type of discount per line.")
                )

    @api.depends(
        "product_uom_qty", "discount", "price_unit", "tax_id", "discount_fixed"
    )
    def _compute_amount(self):
        def _compute_amount(self):
            """
            Compute the amounts of the SO line.
            """
            for line in self:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                                product=line.product_id, partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included']-line.discount_fixed,
                    'price_subtotal': taxes['total_excluded']-line.discount_fixed,
                })
                if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                        'account.group_account_manager'):
                    line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({"discount_fixed": self.discount_fixed})
        return res
