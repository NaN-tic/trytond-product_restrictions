# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['RestrictionCustomer', 'RestrictionSupplier', 'Party']


class RestrictionCustomer(ModelSQL):
    'Product Restriction - Customer'
    __name__ = 'product.restriction-party.party.customer'
    restriction = fields.Many2One('product.restriction', 'Restriction',
        select=True, required=True, ondelete='CASCADE')
    party = fields.Many2One('party.party', 'Party', select=True, required=True,
        ondelete='CASCADE')


class RestrictionSupplier(ModelSQL):
    'Product Restriction - Supplier'
    __name__ = 'product.restriction-party.party.supplier'
    restriction = fields.Many2One('product.restriction', 'Restriction',
        select=True, required=True, ondelete='CASCADE')
    party = fields.Many2One('party.party', 'Party', select=True, required=True,
        ondelete='CASCADE')


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    customer_restrictions = fields.Many2Many(
        'product.restriction-party.party.customer', 'party', 'restriction',
        'Customer Restrictions')
    supplier_restrictions = fields.Many2Many(
        'product.restriction-party.party.supplier', 'party', 'restriction',
        'Supplier Restrictions')
