from decimal import Decimal as D
from django.utils.translation import ugettext as _
from oscar.apps.shipping.methods import Free, FixedPrice
from oscar.apps.shipping.repository import Repository as CoreRepository

class Standard(FixedPrice):
    code = 'standard'
    name = _("Standard shipping")

class Express(FixedPrice):
    code = 'express'
    name = _("Express shipping")

class Repository(CoreRepository):
    """
    This class is included so that there is a choice of shipping methods.
    Oscar's default behaviour is to only have one which means you can't test
    the shipping features of PayPal.
    """
    methods = [Standard(D('10.00')), Express(D('20.00'))]

    def get_shipping_methods(self, user, basket, shipping_addr=None, **kwargs):
        return self.prime_methods(basket, self.methods)

    def find_by_code(self, code, basket):
        for method in self.methods:
            if code == method.code:
                return self.prime_method(basket, method)