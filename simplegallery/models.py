from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.auth.models import Group
from cms.models import Page
from cms.models import CMSPlugin
from cms.models.fields import PageField
from django.utils.text import truncate_words
from multilingual.translation import TranslationModel

from filer.fields.image import FilerImageField

from simplegallery.fields import AspectRatioField

from tinymce.models import HTMLField
from simplegallery import south_introspections # make sure south knows about the HTMLField

CMSPLUGIN_SIMPLE_GALLERY_STYLE_CHOICES = getattr( settings, 'CMSPLUGIN_SIMPLE_GALLERY_STYLE_CHOICES',() )

class Gallery(models.Model):
    name = models.CharField(max_length=255, unique=True,
        help_text=_("A unique identifier for this gallery, this will only be used in the admin panel."))
    groups = models.ManyToManyField(Group, blank=True)
    
    class Translation(TranslationModel):
        title = models.CharField(_('title'), max_length=255, blank=True, default='')
        description = HTMLField(blank=True, default='')

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __unicode__(self):
        return self.name
    
    def has_drop_up(self):
        if not hasattr(self, '_has_drop_up'):
            self._has_drop_up = bool(self.images.filter(drop_up_links__isnull=False).count())
        return self._has_drop_up
        

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, related_name="images")
    image = FilerImageField()
    page_link = PageField(verbose_name=_('page link'), null=True, blank=True)
    free_link = models.CharField(_("link"), max_length=2048, blank=True, null=True, 
                                 help_text=_("an absolute url"))
    ordering = models.IntegerField(null=True, blank=True)
    drop_up_links = models.ManyToManyField('sites.Site', blank=True)
    
    class Translation(TranslationModel):
        title = models.CharField(_('title'), max_length=255, blank=True, default='')
        description = HTMLField(_('description'), blank=True, default='')

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __unicode__(self):
        if isinstance(self.title, basestring):
            return self.title
        return unicode(self.pk)

    @property
    def file(self):
        return self.image.file
    
    @property
    def link(self):
        if self.free_link:
            return self.free_link
        elif self.page_link and self.page_link:
            return self.page_link.get_absolute_url()
        else:
            return ''
    
aspect_ratio_choices = getattr(settings, "IMAGE_ASPECT_RATIO_CHOICES", (
    (1, '1:1'),
    (1.33333, '4:3'),
    (1.77777, '16:9'),
))


class GalleryPublication(CMSPlugin):
    gallery = models.ForeignKey(Gallery)
    interval = models.PositiveSmallIntegerField(_('interval'), default=0)
    style = models.CharField(_("gallery style"), max_length=255, blank=True, choices=CMSPLUGIN_SIMPLE_GALLERY_STYLE_CHOICES)
    aspect_ratio = models.FloatField(_('aspect ratio'), choices=aspect_ratio_choices, default=1)
    raw_aspect_ratio = AspectRatioField(null=True, blank=True, max_length=20)
    
    def get_aspect_ratio(self):
        if self.raw_aspect_ratio:
            x,y = self.raw_aspect_ratio
            return float(x) / float(y)
        return self.aspect_ratio
    
class CarouselImage(models.Model):
    carousel_feature = models.ForeignKey('CarouselFeature', related_name="images")
    image = FilerImageField()
    date = models.DateField(_('date'), null=True, blank=True)
    title = models.CharField(_('title'), max_length=150, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    #title_2 = models.CharField(_('title 2'), max_length=150, null=True, blank=True)
    #description_2 = models.TextField(_('description 2'), null=True, blank=True)
    page_link = PageField(verbose_name=_('page link'), null=True, blank=True)
    free_link = models.CharField(_("link"), max_length=2048, blank=True, null=True, 
                                 help_text=_("an absolute url"))
    url = models.URLField(_('URL'), blank=True, \
        help_text=_('If the %(page_link)s field is not used, you can enter an external URL here.') % {'page_link': _('page link')})
    ordering = models.PositiveSmallIntegerField(_('ordering'), null=True, blank=True)
    
    class Meta:
        ordering = ('ordering',)
        verbose_name = _('carousel image')
        verbose_name_plural = _('carousel images')

    def __unicode__(self):
        return self.title

    @property
    def file(self):
        return self.image.file
    
    def get_url(self):
        if self.page_link:
            return self.page_link.get_absolute_url()
        elif self.url:
            return self.url
    @property
    def link(self):
        if self.free_link:
            return self.free_link
        elif self.page_link and self.page_link:
            return self.page_link.get_absolute_url()
        else:
            return ''
    
class CarouselFeature(CMSPlugin):
    title = models.CharField(_('title'), max_length=50, blank=True)
    interval = models.PositiveSmallIntegerField(_('interval'), default=3)
    aspect_ratio = models.FloatField(_('aspect ratio'), choices=aspect_ratio_choices, default=1)
    
    def __unicode__(self):
        return truncate_words(self.title, 3)[:20] + "..."
    
    def get_aspect_ratio(self):
        return self.aspect_ratio
