from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.utils.functional import curry
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django import forms
from multilingual.admin import (
    MultilingualInlineAdmin, MultilingualModelAdmin, MultilingualModelAdminForm,
    MultilingualInlineModelForm
)
from cms.models import Page
from simplegallery.models import Gallery, Image


class ImageInlineForm(MultilingualInlineModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageInlineForm, self).__init__(*args, **kwargs)
        choices = [(s.id, s.name) for s in Site.objects.all()]
        self.fields['drop_up_links'].widget = forms.SelectMultiple(choices=choices)


class ImageInline(MultilingualInlineAdmin):
    model = Image
    form = ImageInlineForm
    num_in_admin = 20 
    extra = 4 
    raw_id_fields = ('image',) # workaround... because otherwise admin will render an "addlink" after the field
    
    def queryset(self, request):
        return self.model._default_manager.all()
    
    
class GalleryAdminForm(MultilingualModelAdminForm):
    current_request = None
    class Meta:
        model = Gallery
        
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        data = kwargs.get('data', None)
        if instance:
            base_groups = [g.pk for g in instance.groups.all()]
        elif data:
            base_groups = data.get('groups', [])
        else:
            base_groups = []
        initial = kwargs.get('initial') or {}
        initial.update({'groups': [g.pk for g in self.current_request.user.groups.all()] + base_groups})
        kwargs['initial'] = initial
        super(GalleryAdminForm, self).__init__(*args, **kwargs)
        
    def clean_groups(self):
        groups = self.cleaned_data['groups']
        if not (self.current_request.user.groups.filter(pk__in=groups).count() or
                self.current_request.user.is_superuser):
            raise forms.ValidationError("You must choose at least one group you are in.")
        return groups
    

class GalleryAdmin(MultilingualModelAdmin):
    form = GalleryAdminForm
    inlines = [
        ImageInline,
    ]
    list_display = ('name', 'description', 'display_groups')
    search_fields = ('name', 'translations__title','translations__description',)
    # using ordering somehow results in double querysets
#    ordering = ('translations__title', )
    use_fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Language Dependent', {
            'fields': ('title', 'description'),
        }),
        ('Groups', {
            'classes': ('collapse',),
            'fields': ('groups',),
        }),
    )

    def display_groups(self, obj):
        return ', '.join([str(g) for g in obj.groups.all()])
    
    def queryset(self, request):
        qs = super(GalleryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(groups__in=request.user.groups.all()).distinct()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(GalleryAdmin, self).get_form(request, obj=None, **kwargs)
        form.current_request = request
        return form

admin.site.register(Gallery, GalleryAdmin)