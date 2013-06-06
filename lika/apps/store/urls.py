from django.conf.urls import patterns, include, url

urlpatterns = patterns('store.views',
    url(r'^$', 'index', name='home'),    
)
