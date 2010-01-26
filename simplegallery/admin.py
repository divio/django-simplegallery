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

admin.site.register(Gallery, GalleryAdmin)