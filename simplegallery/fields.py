from django.db.models.fields import CharField
from django.forms.fields import RegexField
from django.utils.translation import ugettext_lazy
from django.core import exceptions
import re

ASPECT_RATIO_RE = re.compile('[1-9]\d*:[1-9]\d*') 

class AspectRatioField(CharField):
    def to_python(self, value):
        if isinstance(value, basestring):
            return [int(x) for x in value.split(':')]
        if value is None:
            if self.null:
                return value
            else:
                raise exceptions.ValidationError(
                    ugettext_lazy("This field cannot be null."))
        return self.to_python(smart_unicode(value))

    def formfield(self, **kwargs):
        defaults = {'form_class': RegexField, 'regex': ASPECT_RATIO_RE}
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