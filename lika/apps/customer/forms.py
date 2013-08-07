from django import forms
from django.utils.translation import ugettext_lazy as _


class EmailForm(forms.Form):
    """
    """
    email = forms.EmailField(label=_('please enter the email you used to make the purchase in order to get access to the files'))