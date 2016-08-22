# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
import unittest
import trytond.tests.test_tryton
from trytond.error import UserError
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction


class TestCase(ModuleTestCase):
    'Test module'
    module = 'product_restrictions'

    @with_transaction()
    def test_restrictions(self):
        'Test restrictions'
        pool = Pool()
        Party = pool.get('party.party')
        Template = pool.get('product.template')
        Restriction = pool.get('product.restriction')
        Uom = pool.get('product.uom')

        restriction = Restriction(name='Inflamable Products')
        restriction.save()
        parties = Party.create([{
                    'name': 'Not Restricted Party',
                    }, {
                    'name': 'Supplier',
                    'supplier_restrictions': [('add', [restriction.id])],
                    }, {
                    'name': 'Customer',
                    'customer_restrictions': [('add', [restriction.id])],
                    }])
        free_party, supplier, customer = parties
        unit, = Uom.search([('symbol', '=', 'u')])
        free_template, restricted_template = Template.create([{
                    'name': 'Free Template',
                    'default_uom': unit,
                    'list_price': Decimal(0),
                    'cost_price': Decimal(0),
                    }, {
                    'name': 'Restricted Template',
                    'default_uom': unit,
                    'list_price': Decimal(0),
                    'cost_price': Decimal(0),
                    'restrictions': [('add', [restriction.id])],
                    }])

        for party in parties:
            Template.check_product_restrictions([free_template], party)
            Template.check_product_restrictions([free_template], party,
                    type='supplier')

        with self.assertRaises(UserError):
            Template.check_product_restrictions([restricted_template],
                free_party)

        with self.assertRaises(UserError):
            Template.check_product_restrictions([restricted_template],
                free_party, type='supplier')

        templates = [free_template, restricted_template]
        for party in [free_party, supplier]:
            with self.assertRaises(UserError):
                Template.check_product_restrictions(templates, party)
        for party in [free_party, customer]:
            with self.assertRaises(UserError):
                Template.check_product_restrictions(templates, party,
                    type='supplier')

        Template.check_product_restrictions([restricted_template],
            customer)
        Template.check_product_restrictions([restricted_template],
            supplier, type='supplier')


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
