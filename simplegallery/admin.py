from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.utils.functional import curry
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django import forms
from multilingual.admin import (
    MultilingualInlineAdmin, MultilingualModelAdmin, MultilingualModelAdminForm,
    MultilingualInlineModelForm
)
from cms.models import Page
from simplegallery.models import Gallery, Image
from django.core.cache import cache

PAGE_LINK_CACHE_KEY = 'sg_ii_pl_qs' # simple gallery image inline page link query set

class ImageInlineForm(MultilingualInlineModelForm):
    def clean_page_link(self):
        pageid = self.cleaned_data.get('page_link','')
        if not pageid:
            return None
        page = Page.objects.get(pk=pageid)
        return page
    
    class Meta:
        model = Image


class ImageInline(MultilingualInlineAdmin):
    model = Image
    num_in_admin = 20 
    extra = 4 
    max_num = 40
    raw_id_fields = ('image',) # workaround... because otherwise admin will render an "addlink" after the field
    form = ImageInlineForm
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ImageInline, self).get_formset(request, obj, **kwargs)
        choices = cache.get(PAGE_LINK_CACHE_KEY)
        if choices is None:
            current_site = None
            choices = [('', '----')]
            current = []
            for page in formset.form.base_fields['page_link'].queryset.drafts():
                if page.site != current_site:
                    if current:
                        choices.append((current_site.name, current))
                        current = []
                    current_site = page.site
                current.append((page.pk, unicode(page)))
            if current:
                choices.append((current_site.name, current))
            cache.set(PAGE_LINK_CACHE_KEY, choices, 86400)
        formset.form.base_fields['page_link'] = forms.ChoiceField(choices=choices, required=False, label=_("page link"))
        return formset
    
    
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
    search_fields = ('translations__title','translations__description',)
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