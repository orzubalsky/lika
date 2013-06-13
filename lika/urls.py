from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app import application
from paypal.payflow.app import application as payflow
from paypal.express.dashboard.app import application as express_dashboard

admin.autodiscover()

# direct browser requests to the different apps
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    # PayPal Express integration...
    (r'^checkout/paypal/', include('paypal.express.urls')),
    # Dashboard views for Payflow Pro
    (r'^dashboard/paypal/payflow/', include(payflow.urls)),
    # Dashboard views for Express
    (r'^dashboard/paypal/express/', include(express_dashboard.urls)),
    (r'', include(application.urls)),
)

# static files url patterns
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
   )
