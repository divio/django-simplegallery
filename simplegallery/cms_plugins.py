from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from simplegallery.models import GalleryPublication, CarouselImage,\
    CarouselFeature, Gallery
from django.template.defaultfilters import title

class SimpleGalleryPublicationPlugin(CMSPluginBase):
    model = GalleryPublication
    name = _("Gallery")
    render_template = "simplegallery/gallery_plugin.html"
    change_form_template = "simplegallery/plugin_form.html"
    text_enabled = False
    
    if not getattr(settings, 'CMSPLUGIN_SIMPLE_GALLERY_STYLE_CHOICES', False):
        exclude = ('style',)
    
    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'gallery': instance.gallery,
            'images': instance.gallery.images.all(),
            'image_size': get_image_size(context, instance),
            'placeholder': placeholder,
        })
        return context
        
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey.
        """
        gallery = self.model.gallery.field
        if request and db_field is gallery and not request.user.is_superuser:
            kwargs['queryset'] = Gallery.objects.filter(groups__in=request.user.groups.all()).distinct()
        else:
            kwargs['queryset'] = Gallery.objects.all()
        return super(SimpleGalleryPublicationPlugin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    """
    class PluginMedia:
        css = {
            'all': ('%ssimplegallery/css/simplegallery.css' % settings.MEDIA_URL,)
        }
    """
 
plugin_pool.register_plugin(SimpleGalleryPublicationPlugin)

class CarouselImageInline(admin.StackedInline):
    model = CarouselImage
    fk_name = 'carousel_feature'
    extra = 1

class CarouselFeaturePlugin(CMSPluginBase):
    model = CarouselFeature
    name = title(_('Gallery lite'))
    placeholders = ('feature_home',)
    render_template = "simplegallery/gallery_lite.html"
    change_form_template = "simplegallery/plugin_form.html"
    text_enabled = False
    inlines = [
        CarouselImageInline,
    ]
    
    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'images': instance.images.all(),
            'image_size': get_image_size(context, instance),
            'placeholder': placeholder,
        })
        return context
    
    class PluginMedia:
        '''
        js = ('%ssimplegallery/js/jquery.cycle.min.js'% settings.MEDIA_URL,
              '%ssimplegallery/js/jquery.cycle.trans.min.js'% settings.MEDIA_URL,)
        '''
plugin_pool.register_plugin(CarouselFeaturePlugin)

def get_image_size(context, instance):
    placeholder_width = context.get('width', None)
    if placeholder_width:
        width = placeholder_width
    else:
        try:
            width = instance.image.width
        except:
            width = 100
    try:
        width = int(float(width))
    except ValueError:
        width = 100
    height = int(round(float(width) / instance.get_aspect_ratio()))
    return (u'%dx%d' % (width, height), width, height)
