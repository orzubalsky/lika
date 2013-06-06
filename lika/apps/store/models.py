from django.db.models import *
from datetime import *


class Base(Model):
    """
    Base model for all of the models in ts.  
    """
    class Meta:
            abstract = True
                    
    created     = DateTimeField(auto_now_add=True, editable=False)
    updated     = DateTimeField(auto_now=True, editable=False)
    is_active   = BooleanField(default=1)        
        
    def __unicode__ (self):
        if hasattr(self, "title") and self.title:
            return self.title
        else:
            return "%s" % (type(self))