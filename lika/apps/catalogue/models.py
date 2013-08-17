from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.db.models import *


class Product(AbstractProduct):

    DIFFICULTY_CHOICES = (
        ('beginner', 'beginner'),
        ('medium', 'medium'),
        ('advanced', 'advanced'),
    )


    filename = FileField(upload_to='files', null=True, blank=True)
    vimeo = TextField(verbose_name=u'vimeo embed code', blank=True, null=True)
    difficulty_level = CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True, null=True, default='beginner')


from oscar.apps.catalogue.models import *