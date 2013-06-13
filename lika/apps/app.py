from oscar.app import Shop

from checkout.app import application as checkout_app


class PayPalShop(Shop):
    checkout_app = checkout_app

application = PayPalShop()
