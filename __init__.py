# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .product import *
from .party import *


def register():
    Pool.register(
        Restriction,
        RestrictionTemplate,
        Template,
        RestrictionCustomer,
        RestrictionSupplier,
        Party,
        Sale,
        Purchase,
        ShipmentIn,
        ShipmentInReturn,
        ShipmentOut,
        ShipmentOutReturn,
        module='product_restrictions', type_='model')
