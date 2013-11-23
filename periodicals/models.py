# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.db.models import permalink
from django.conf import settings
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from autoslug.fields import AutoSlugField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
try:
    # use tagging_autocomplete if it is installed
    from tagging_autocomplete.models import TagAutocompleteField as TagField
except ImportError:
    pass


class ActiveLinkManager(models.Manager):
    def get_query_set(self):
        return super(ActiveLinkManager, self).get_query_set().filter(status=self.model.STATUS_ACTIVE)


class LinkItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    STATUS_SUBMITTED = 'S'
    STATUS_ACTIVE = 'A'
    STATUS_DELETED = 'D'
    STATUS_CHOICES = (
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DELETED, 'Deleted'),
    )
    status = models.CharField(verbose_name=_('status'),
                              max_length=1,
                              choices=STATUS_CHOICES,
                              default=STATUS_SUBMITTED)

    url = models.URLField(_("url"), blank=True)
    title = models.CharField(_("title"), max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Define first so admin shows all regardless of status
    objects = models.Manager()
    active = ActiveLinkManager()

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('periodicals_article_detail', (), {'periodical_slug':self.issue.periodical.slug,
                                                   'issue_slug':self.issue.slug,
                                                   'slug':self.slug})

TITLE_CHOICES = (
    ('MR', _('Mr.')),
    ('MRS', _('Mrs.')),
    ('MS', _('Ms.')),
    ('DR', _('Dr.')),
)


class Author(models.Model):
    title = models.CharField(_("title"), max_length=3, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(_("first name"), max_length=100)
    middle_name = models.CharField(_("middle name"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=100)
    postnomial = models.CharField(_("postnomial"), max_length=100, blank=True, help_text=_("i.e. PhD, DVM"))
    website = models.URLField(_("website"), blank=True)
    alt_website = models.URLField(_("website"), blank=True, help_text=_("Alternate website for this author"))
    blog = models.URLField(_("blog"), blank=True)
    email = models.EmailField(_("email"), blank=True)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        unique_together = ("title", "first_name",
                           "middle_name", "last_name",
                           "postnomial")
        ordering = ('last_name',)

    def __unicode__(self):
        return "%s %s %s %s " % (self.last_name,
                                 self.first_name,
                                 self.middle_name,
                                 self.postnomial)

    @permalink
    def get_absolute_url(self):
        return ('periodicals_author_detail', (), {'slug':self.slug})

    def save(self, force_insert=False, force_update=False):
        if not self.id and not self.slug: # use the user's slug if supplied
            # don't transmogrify slug/URL on update

                self.slug = slugify(" ".join([self.last_name,
                                              self.first_name,
                                              self.middle_name,
                                              self.postnomial]))
        super(Author, self).save(force_insert, force_update)

    def get_name_display(self):
        if self.first_name or self.middle_name or self.postnomial:
            return "%s, %s %s %s " % (self.last_name,
                                      self.first_name,
                                      self.middle_name,
                                      self.postnomial)
        else:
            return self.last_name  # no comma


def logo_upload(instance, filename):
    full_path = "%s/logo" % (instance.name.lower())
    return full_path

class Periodical(models.Model):
    name = models.CharField(_("name"), max_length=100)
    publisher = models.CharField(_("publisher"), max_length=100, blank=True)
    address_1 = models.CharField(_("address_1"), max_length=100, blank=True)
    address_2 = models.CharField(_("address_2"), max_length=100, blank=True)
    city = models.CharField(_("city"), max_length=100, blank=True)
    state = models.CharField(_("state"), max_length=100, blank=True)
    country = models.CharField(_("country"), max_length=100, blank=True)
    zipcode = models.CharField(_("zipcode"), max_length=10, blank=True)
    website = models.URLField(_("website"), blank=True)
    logo = models.ImageField(upload_to=logo_upload, blank=True, max_length=200)
    blog = models.URLField(_("blog"), blank=True)
    email = models.EmailField(_("email"), blank=True)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)

    class Meta:
        verbose_name = _('periodical')
        verbose_name_plural = _('periodicals')

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('periodicals_periodical_detail', (), {'slug':self.slug})

    def save(self, force_insert=False, force_update=False):
        # don't transmogrify slug/URL on update
        if not self.id and not self.slug: # use the user's slug if supplied
                self.slug = slugify(self.name)
        super(Periodical, self).save(force_insert, force_update)


def issue_upload_to(instance, filename, suffix):
    full_path = "%s/issues/%s-%s-%s" % (instance.periodical.name.lower().replace(' ', ''),
                                        instance.get_year_display(),
                                        instance.get_month_display() or slugify(instance.title),
                                        suffix)
    return full_path

def issue_upload_print(instance, filename):
    return issue_upload_to(instance, filename, "print")

def issue_upload_digital(instance, filename):
    return issue_upload_to(instance, filename, "digital")

class Issue(models.Model):
    periodical = models.ForeignKey('Periodical')
    volume = models.PositiveIntegerField(_("volume"))
    issue = models.PositiveIntegerField(_("issue"))
    pub_date = models.DateField(default=datetime.datetime.now)
    title = models.CharField(_("title"), max_length=100, blank=True, help_text=_("title for special issues"))
    description = models.TextField(_("description"), max_length=200, blank=True)
    printed_cover = models.ImageField(upload_to=issue_upload_print, blank=True, max_length=200, help_text=_("Upload image of printed issue's cover"))
    buy_print = models.URLField(_("buy print"), blank=True, help_text=_("URL to buy print issue"))
    digital_cover = models.ImageField(upload_to=issue_upload_digital, blank=True, max_length=200, help_text=_("Upload image of digital issue's cover"))
    buy_digital = models.URLField(_("buy digital"), blank=True, help_text=_("URL to buy digital issue"))
    read_online = models.URLField(_("read online"), blank=True, help_text=_("URL to read online issue"))
    slug = models.SlugField(max_length=200, unique_for_month="pub_date",
                            help_text=_("this field is automatically generated when saved"),
                            blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    links = generic.GenericRelation(LinkItem)

    class Meta:
        verbose_name = _('issue')
        verbose_name_plural = _('issues')
        ordering = ('-pub_date',)

    def __unicode__(self):
        return "%s %d.%d %s" % (self.periodical,
                                self.volume,
                                self.issue,
                                self.pub_date.strftime("%Y-%b"))

    @permalink
    def get_absolute_url(self):
        return ('periodicals_issue_detail', (), {'periodical_slug':self.periodical.slug,
                                                 'slug':self.slug,
                                                 })

    def save(self, force_insert=False, force_update=False):
        # slugifying in save so data imported via fixtures gets slugged
        if not self.id and not self.slug: # use the user's slug if supplied
                if self.title:
                    # special issues
                    self.slug = slugify(self.title)
                else:
                    # regular issues
                    self.slug = slugify("%(volume)s %(issue)s" % self.__dict__)
        super(Issue, self).save(force_insert, force_update)

    def get_name_display(self):
        if self.title:
            return self.title
        else:
            return _("%s Vol. %s No. %s" % (self.get_month_display(), self.volume, self.issue))

    def get_date_display(self):
        return self.get_year_display() + " - " + self.get_month_display()

    def get_year_display(self):
        return self.pub_date.strftime("%Y")

    def get_month_display(self):
        if self.title:
            return ""
        else:
            return self.pub_date.strftime("%b")

    def active_links(self):
        return [link for link in self.links.all() if link.status == LinkItem.STATUS_ACTIVE]


def article_upload_image(instance, filename):
    full_path = "%s/articles/%s" % (instance.issue.periodical.name.lower(),
                                    instance.slug.lower())
    return full_path

class Article(models.Model):
    series = models.CharField(_("series"), max_length=100)
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), max_length=200, blank=True)
    page = models.PositiveIntegerField(_("page"), blank=True, null=True)
    tags = TagField()
    image = models.ImageField(upload_to=article_upload_image, blank=True, max_length=200, help_text=_("Upload image associated with article"))
    buy_print = models.URLField(_("buy print"), blank=True, help_text=_("URL to buy print article"))
    buy_digital = models.URLField(_("buy digital"), blank=True, help_text=_("URL to buy digital article"))
    read_online = models.URLField(_("read online"), blank=True, help_text=_("URL to read online article"))
    issue = models.ForeignKey('Issue', related_name='articles')
    authors = models.ManyToManyField('Author', related_name='articles')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(max_length=200,
                         populate_from='title',
                         unique=True,
                         editable=True,
                         help_text=_("this field is automatically generated when saved"),
                         blank=True)
    links = generic.GenericRelation(LinkItem)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __unicode__(self):
        return " %s - %s" % (self.issue, self.title)

##     def save(self, force_insert=False, force_update=False):
##         if not self.id and not self.slug: # use the user's slug if supplied
##             self.slug = slugify(self.title)
##         super(Article, self).save(force_insert, force_update)

    @permalink
    def get_absolute_url(self):
        return ('periodicals_article_detail', (), {'periodical_slug':self.issue.periodical.slug,
                                                   'issue_slug':self.issue.slug,
                                                   'slug':self.slug})
    def active_links(self):
        return [link for link in self.links.all() if link.status == LinkItem.STATUS_ACTIVE]
