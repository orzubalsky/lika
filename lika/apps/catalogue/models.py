from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.db.models import *


class Product(AbstractProduct):
    filename = FileField(upload_to='files')


from oscar.apps.catalogue.models import *