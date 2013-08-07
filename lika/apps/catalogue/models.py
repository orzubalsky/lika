from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.db.models import *


class Product(AbstractProduct):
    filename = FileField(upload_to='files', null=True, blank=True)
    vimeo 	 = TextField(verbose_name=u'vimeo embed code', blank=True, null=True)


from oscar.apps.catalogue.models import *