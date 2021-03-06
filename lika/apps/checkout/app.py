from oscar.apps.checkout import app

from checkout import views


class CheckoutApplication(app.CheckoutApplication):
    payment_details_view = views.PaymentDetailsView
    shipping_method_view = views.ShippingMethodView

application = CheckoutApplication()
