from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from oscar.app import application

admin.autodiscover()

# direct browser requests to the different apps
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    (r'^checkout/paypal/', include('paypal.express.urls')),    
    (r'', include(application.urls))
)

# static files url patterns
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, }),
   )
