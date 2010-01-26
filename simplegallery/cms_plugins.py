from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf import settings
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from simplegallery.models import GalleryPublication, CarouselImage,\
    CarouselFeature
from django.template.defaultfilters import title

class SimpleGalleryPublicationPlugin(CMSPluginBase):
    model = GalleryPublication
    name = _("SimpleGallery Publication")
    render_template = "simplegallery/gallery_plugin.html"
    change_form_template = "simplegallery/plugin_form.html"
    text_enabled = False 
    
    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'gallery': instance.gallery,
            'image_size': get_image_size(context, instance),
            'placeholder': placeholder,
        })
        return context
    
    class PluginMedia:
        css = {
            'all': ('%scss/jquery.lightbox-0.5.css' % settings.MEDIA_URL,)
        }
        js = ('%ssimplegallery/js/jquery.cycle.min.js'% settings.MEDIA_URL,
              '%ssimplegallery/js/jquery.cycle.trans.min.js'% settings.MEDIA_URL,
              '%ssimplegallery/js/jquery.lightbox-0.5.min.js'% settings.MEDIA_URL,)
 
plugin_pool.register_plugin(SimpleGalleryPublicationPlugin)

class CarouselImageInline(admin.StackedInline):
    model = CarouselImage
    fk_name = 'carousel_feature'
    extra = 1
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CarouselImageInline, self).get_formset(request, obj, **kwargs)
        formset.form.base_fields['page_link'].queryset = formset.form.base_fields['page_link'].queryset.drafts()
        return formset

class CarouselFeaturePlugin(CMSPluginBase):
    model = CarouselFeature
    name = title(_('carousel image feature'))
    placeholders = ('feature_home',)
    render_template = "simplegallery/feature_plugin.html"
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
        print get_image_size(context, instance)
        return context
    
    class PluginMedia:
        js = ('%ssimplegallery/js/jquery.cycle.min.js'% settings.MEDIA_URL,
              '%ssimplegallery/js/jquery.cycle.trans.min.js'% settings.MEDIA_URL,)
 
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
    height = int(float(width) / instance.aspect_ratio)
    return (u'%sx%s' % (width, height), width, height)