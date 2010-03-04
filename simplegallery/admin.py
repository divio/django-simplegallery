from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.utils.functional import curry
from django.forms.models import inlineformset_factory
import multilingual
from simplegallery.models import Gallery, Image

class ImageInline(multilingual.MultilingualInlineAdmin):
    model = Image
    num_in_admin = 20 
    extra = 4 
    max_num = 40
    raw_id_fields = ('image',) # workaround... because otherwise admin will render an "addlink" after the field
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ImageInline, self).get_formset(request, obj, **kwargs)
        formset.form.base_fields['page_link'].queryset = formset.form.base_fields['page_link'].queryset.drafts()
        return formset

class GalleryAdmin(multilingual.MultilingualModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ('name', 'description',)
    search_fields = ('translations__title','translations__description',)
    # using ordering somehow results in double querysets
#    ordering = ('translations__title', )
    
    def queryset(self, request):
        qs = super(GalleryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(groups__in=request.user.groups.all())
    
    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        obj = super(GalleryAdmin, self).save_form(request, form, change)
        obj.save()
        if not obj.groups.count():
            obj.groups.add(*request.user.groups.all())
        return obj

admin.site.register(Gallery, GalleryAdmin)