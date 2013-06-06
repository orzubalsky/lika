from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.conf import settings
from django.template.defaultfilters import slugify
from datetime import *
from store.models import *
from store.forms import *

def index(request):
    pass