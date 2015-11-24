# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta, Pool

__all__ = ['Restriction', 'RestrictionTemplate', 'Template', 'Sale',
    'Purchase', 'ShipmentIn', 'ShipmentInReturn', 'ShipmentOut',
    'ShipmentOutReturn']
__metaclass__ = PoolMeta


class Restriction(ModelSQL, ModelView):
    'Product Restriction'
    __name__ = 'product.restriction'
    name = fields.Char('Name', required=True)


class RestrictionTemplate(ModelSQL):
    'Product Restriction - Product Template'
    __name__ = 'product.restriction-product.template'
    restriction = fields.Many2One('product.restriction', 'Restriction',
        select=True, required=True, ondelete='CASCADE')
    template = fields.Many2One('product.template', 'Template',
        select=True, required=True, ondelete='CASCADE')


class Template:
    __name__ = 'product.template'
    restrictions = fields.Many2Many('product.restriction-product.template',
        'template', 'restriction', 'Restrictions')

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls._error_messages.update({
                'restricted_product': ('Product "%(product)s" can not be '
                    'moved from/to party "%(party)s" because it misses '
                    'restriction "%(restriction)s".'),
                })

    @classmethod
    def check_product_restrictions(cls, products, party, type='customer'):
        party_restrictions = set(getattr(party, '%s_restrictions' % type))
        for product in products:
            product_restrictions = set(product.restrictions)
            if not product_restrictions:
                continue
            missing = product_restrictions - party_restrictions
            if missing:
                restriction = missing.pop()
                cls.raise_user_error('restricted_product', {
                        'product': product.rec_name,
                        'party': party.rec_name,
                        'restriction': restriction.rec_name,
                        })


class Sale:
    __name__ = 'sale.sale'

    @classmethod
    def quote(cls, sales):
        pool = Pool()
        Template = pool.get('product.template')
        for sale in sales:
            products = list(set(l.product.template for l in sale.lines
                    if l.product))
            Template.check_product_restrictions(products, sale.party)
        super(Sale, cls).quote(sales)


class Purchase:
    __name__ = 'purchase.purchase'

    @classmethod
    def quote(cls, purchases):
        pool = Pool()
        Template = pool.get('product.template')
        for purchase in purchases:
            products = list(set(l.product.template for l in purchase.lines
                    if l.product))
            Template.check_product_restrictions(products, purchase.party,
                type='supplier')
        super(Purchase, cls).quote(purchases)


class ShipmentIn:
    __name__ = 'stock.shipment.in'

    @classmethod
    def receive(cls, shipments):
        pool = Pool()
        Template = pool.get('product.template')
        for shipment in shipments:
            products = list(set(l.product.template
                    for l in shipment.incoming_moves))
            Template.check_product_restrictions(products, shipment.supplier,
                type='supplier')
        super(ShipmentIn, cls).receive(shipments)


class ShipmentInReturn:
    __name__ = 'stock.shipment.in.return'

    # TODO: Shipment in return has not party field :(
    # See: https://bugs.tryton.org/issue4035
    #@classmethod
    #def assign(cls, shipments):
    #    pool = Pool()
    #    Template = pool.get('product.template')
    #    for shipment in shipments:
    #        products = list(set(l.product.template for l in shipment.moves))
    #        Template.check_product_restrictions(products, shipment.supplier,
    #            type='supplier')
    #    super(ShipmentInReturn, cls).assign(shipments)


class ShipmentOut:
    __name__ = 'stock.shipment.out'

    @classmethod
    def pack(cls, shipments):
        pool = Pool()
        Template = pool.get('product.template')
        for shipment in shipments:
            products = list(set(l.product.template
                    for l in shipment.inventory_moves))
            Template.check_product_restrictions(products, shipment.customer)
        super(ShipmentOut, cls).pack(shipments)

    @classmethod
    def do(cls, shipments):
        pool = Pool()
        Template = pool.get('product.template')
        for shipment in shipments:
            products = list(set(l.product.template
                    for l in shipment.outgoing_moves))
            Template.check_product_restrictions(products, shipment.customer)
        super(ShipmentOut, cls).do(shipments)


class ShipmentOutReturn:
    __name__ = 'stock.shipment.out.return'

    @classmethod
    def receive(cls, shipments):
        pool = Pool()
        Template = pool.get('product.template')
        for shipment in shipments:
            products = list(set(l.product.template
                    for l in shipment.incoming_moves))
            Template.check_product_restrictions(products, shipment.customer,
                type='supplier')
        super(ShipmentOutReturn, cls).receive(shipments)
