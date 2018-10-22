# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['RestrictionCustomer', 'RestrictionSupplier', 'PartyCustomer',
    'PartySupplier']


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
    __metaclass__ = PoolMeta
    restriction = fields.Many2One('product.restriction', 'Restriction',
        select=True, required=True, ondelete='CASCADE')
    party = fields.Many2One('party.party', 'Party', select=True, required=True,
        ondelete='CASCADE')


class PartyCustomer:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta
    customer_restrictions = fields.Many2Many(
        'product.restriction-party.party.customer', 'party', 'restriction',
        'Customer Restrictions')


class PartySupplier:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta
    supplier_restrictions = fields.Many2Many(
        'product.restriction-party.party.supplier', 'party', 'restriction',
        'Supplier Restrictions')
