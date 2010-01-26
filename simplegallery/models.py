from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.models import Page
from cms.models import CMSPlugin
from django.utils.text import truncate_words
import multilingual

from filer.fields.image import FilerImageField

class Gallery(models.Model):
    name = models.CharField(max_length=255, unique=True,
        help_text=_("A unique identifier for this gallery, this will only be used in the admin panel."))
    class Translation(multilingual.Translation):
        title = models.CharField(max_length=255, null=True, blank=True)
        description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __unicode__(self):
        return self.name

class Image(models.Model):
    gallery = models.ForeignKey(Gallery, related_name="images")
    image = FilerImageField()
    page_link = models.ForeignKey(Page, verbose_name=_('page link'), null=True, blank=True)
    ordering = models.IntegerField(null=True, blank=True)
    
    class Translation(multilingual.Translation):
        title = models.CharField(_('title'), max_length=255, null=True, blank=True)
        description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        ordering = ('ordering',)
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __unicode__(self):
        return self.title

    @property
    def file(self):
        return self.image.file
    
aspect_ratio_choices = getattr(settings, "IMAGE_ASPECT_RATIO_CHOICES", (
    (1, '1:1'),
    (1.33333, '4:3'),
    (1.77777, '16:9'),
))


class GalleryPublication(CMSPlugin):
    gallery = models.ForeignKey(Gallery)
    aspect_ratio = models.FloatField(_('aspect ratio'), choices=aspect_ratio_choices, default=1)
    
    def __unicode__(self):
        return u"publication of %s on %s" % (self.gallery, self.page)
    
class CarouselImage(models.Model):
    carousel_feature = models.ForeignKey('CarouselFeature', related_name="images")
    image = FilerImageField()
    date = models.DateField(_('date'), null=True, blank=True)
    title = models.CharField(_('title'), max_length=150, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    title_2 = models.CharField(_('title 2'), max_length=150, null=True, blank=True)
    description_2 = models.TextField(_('description 2'), null=True, blank=True)
    page_link = models.ForeignKey(Page, verbose_name=_('page link'), null=True, blank=True)
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
    
class CarouselFeature(CMSPlugin):
    title = models.CharField(_('title'), max_length=50, blank=True)
    interval = models.PositiveSmallIntegerField(_('interval'), default=3)
    aspect_ratio = models.FloatField(_('aspect ratio'), choices=aspect_ratio_choices, default=1)
    
    def __unicode__(self):
        return truncate_words(self.title, 3)[:20] + "..."