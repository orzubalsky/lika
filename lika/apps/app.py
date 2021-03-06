from django.conf.urls import patterns, url, include
from oscar.app import Shop

from checkout.app import application as checkout_app
from customer.app import application as customer_app

from oscar.core.application import Application
from oscar.apps.catalogue.app import application as catalogue_app
from oscar.apps.basket.app import application as basket_app
from oscar.apps.promotions.app import application as promotions_app
from oscar.apps.search.app import application as search_app
from oscar.apps.offer.app import application as offer_app
from oscar.apps.dashboard.app import application as dashboard_app
from oscar.views.decorators import login_forbidden
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from oscar.apps.customer import forms

class PayPalShop(Shop):
    checkout_app = checkout_app
    catalogue_app = catalogue_app
    customer_app = customer_app
    basket_app = basket_app
    promotions_app = promotions_app
    search_app = search_app
    dashboard_app = dashboard_app
    offer_app = offer_app

    def get_urls(self):
	    urlpatterns = patterns('',
	        (r'^i18n/', include('django.conf.urls.i18n')),
	        (r'^basket/', include(self.basket_app.urls)),
	        (r'^checkout/', include(self.checkout_app.urls)),
	        (r'^accounts/', include(self.customer_app.urls)),
	        (r'^search/', include(self.search_app.urls)),
	        (r'^dashboard/', include(self.dashboard_app.urls)),
	        (r'^offers/', include(self.offer_app.urls)),

	        # Password reset - as we're using Django's default view funtions,
	        # we can't namespace these urls as that prevents
	        # the reverse function from working.
	        url(r'^password-reset/$',
	            login_forbidden(auth_views.password_reset),
	            {'password_reset_form': forms.PasswordResetForm,
	             'post_reset_redirect': reverse_lazy('password-reset-done')},
	            name='password-reset'),
	        url(r'^password-reset/done/$',
	            login_forbidden(auth_views.password_reset_done),
	            name='password-reset-done'),
	        url(r'^password-reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	            login_forbidden(auth_views.password_reset_confirm),
	            {'post_reset_redirect': reverse_lazy('password-reset-complete')},
	            name='password-reset-confirm'),
	        url(r'^password-reset/complete/$',
	            login_forbidden(auth_views.password_reset_complete),
	            name='password-reset-complete'),
	        (r'', include(self.catalogue_app.urls)),
	    )
	    return urlpatterns

application = PayPalShop()
