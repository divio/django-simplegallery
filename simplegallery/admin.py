from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django import forms
from django.core import urlresolvers
from django.http import HttpResponse
from multilingual.admin import (
    MultilingualInlineAdmin, MultilingualModelAdmin, MultilingualModelAdminForm,
    MultilingualInlineModelForm
)
from simplegallery.models import Gallery, Image


def sync_folder(modeladmin, request, queryset):
    for obj in queryset:
        obj.sync_folder()
sync_folder.short_description = "Sync galleries with folders (if selected)"

class ReadOnlyLinkWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        if value:
            return mark_safe(u'<a href="%s" onclick="return showRelatedObjectLookupPopup(this);">%s</a>' % (value, _('edit')))
        else:
            return u''

class ImageInlineForm(MultilingualInlineModelForm):
    admin_edit_url = forms.URLField(label=_('detail edit'), required=False,widget=ReadOnlyLinkWidget)
    def __init__(self, *args, **kwargs):
        super(ImageInlineForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields['admin_edit_url'].initial = urlresolvers.reverse('admin:simplegallery_image_change', args=(self.instance.id,))
    class Meta:
        model = Image
    
class ImageInline(admin.TabularInline):#MultilingualInlineAdmin):
    model = Image
    form = ImageInlineForm
    num_in_admin = 20 
    extra = 4 
    raw_id_fields = ('image',) # workaround... because otherwise admin will render an "addlink" after the field
    fields = ('image','ordering','admin_edit_url',)
    #readonly_fields = ('admin_edit_url',)
    def queryset(self, request):
        return self.model._default_manager.all()
    def edit_detail_link(self, obj):
        return '<a href="#">go bronkos!</a>'

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
    actions = [sync_folder,]
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
        ('Extra', {
            'classes': ('collapse',),
            'fields': ('groups', 'folder'),
        }),
    )
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        if form.instance.folder:
            form.instance.sync_folder()

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

class ReadOnlyImageWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        if value:
            return mark_safe(u'<img src="%s" alt="" />' % (value,))
        else:
            return u''

class ImageDetailForm(MultilingualModelAdminForm):
    image_preview = forms.Field(label=_('image'), required=False, widget=ReadOnlyImageWidget)
    def __init__(self, *args, **kwargs):
        super(ImageDetailForm, self).__init__(*args, **kwargs)
        choices = [(s.id, s.name) for s in Site.objects.all()]
        self.fields['drop_up_links'].widget.choices = choices
        if self.instance and self.instance.id and self.instance.image:
            self.fields['image_preview'].initial = self.instance.image.icons.get('64','')

class ImageDetailAdmin(MultilingualModelAdmin):
    form = ImageDetailForm
    use_fieldsets= (
        (None, {'fields': ('gallery','image_preview',)}),
        (_('links'), {'fields': ('page_link','free_link',)}),
        (None, {'fields': ('title','description',)}),
        (_('advanced'), {'fields': ('drop_up_links',),'classes': ('collapse',),}),
    )
    readonly_fields = ('gallery',)
    filter_horizontal = ('drop_up_links',)
    def response_change(self, request, obj):
        if not request.POST.get("_continue"):
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        return super(ImageDetailAdmin, self).response_change(request, obj)
    def has_add_permission(self, request):
        '''
        Can only be added in the context of a gallery
        '''
        return False
    def has_delete_permission(self, request, obj=None):
        '''
        Can only be deleted in the context of a gallery
        '''
        return False
    def get_model_perms(self, request):
        '''
        The image change view should only be accessable from the edit link
        on the inlines of the gallery change view.
        '''
        return {
            'add': False,
            'change': False,
            'delete': False,
        }

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageDetailAdmin)