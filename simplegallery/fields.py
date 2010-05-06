from django.db import models
from django.forms.fields import RegexField
from django.utils.translation import ugettext_lazy
from django.utils.encoding import smart_unicode
from django.core import exceptions
import re

ASPECT_RATIO_RE = re.compile('[1-9]\d*:[1-9]\d*')


class AspectRatioFormField(RegexField):
    def __init__(self, *args, **kwargs):
        super(AspectRatioFormField, self).__init__(*args, **kwargs)
        self.localize = True
    
    def localize_value(self, value):
        if value:
            return '%s:%s' % tuple(value)
        return value
 

class AspectRatioField(models.CharField):
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        if isinstance(value, list):
            return value
        if isinstance(value, basestring):
            if ':' in value:
                return [int(x) for x in value.split(':')]
            else:
                return None
        if value is None:
            if self.null:
                return value
            else:
                raise exceptions.ValidationError(
                    ugettext_lazy("This field cannot be null."))
        return self.to_python(smart_unicode(value))

    def get_prep_value(self, value):
        if isinstance(value, list):
            return '%s:%s' % tuple(value)
        if isinstance(value, basestring):
            if ':' in value:
                return value
        return None
    
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.get_prep_value(value)

    def value_from_object(self, obj):
        return self.to_python(getattr(obj, self.attname))

    def formfield(self, **kwargs):
        defaults = {'form_class': AspectRatioFormField, 'regex': ASPECT_RATIO_RE}
        if 'initial' in kwargs:
            kwargs['initial'] = self.get_prep_value(kwargs['initial'])
        defaults.update(kwargs)
        return super(AspectRatioField, self).formfield(**defaults)
    
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)