# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import party


def register():
    Pool.register(
        product.Restriction,
        product.RestrictionTemplate,
        product.Template,
        party.Party,
        module='product_restrictions', type_='model')
    Pool.register(
        party.RestrictionCustomer,
        product.Sale,
        product.ShipmentOut,
        product.ShipmentOutReturn,
        depends=['sale'],
        module='product_restrictions', type_='model')
    Pool.register(
        party.RestrictionSupplier,
        product.Purchase,
        product.ShipmentIn,
        depends=['purchase'],
        module='product_restrictions', type_='model')
