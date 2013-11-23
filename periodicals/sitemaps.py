from django.contrib.sitemaps import Sitemap, GenericSitemap
from periodicals.models import Author, Periodical, Issue, Article
from tagging.models import Tag

class StaticPagesSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ['/about_me.html', '/contact.html', '/some-static-url.html']

    def location(self, obj):
        return obj

class SlugSitemap(GenericSitemap):
    """Use for objects that don't implement get_absolute_url but have a slug field used in creating their url"""
    def __init__(self, info_dict, priority=None, changefreq=None):
        GenericSitemap.__init__(self, info_dict, priority=priority, changefreq=changefreq)
        self.url = info_dict.get('url', '/')
        self.slugfield = info_dict['slugfield']
        self.suffix = info_dict.get('suffix', '')

    def location(self, obj):
        return "%s%s%s" % (self.url, getattr(obj, self.slugfield), self.suffix)


class SuffixedSitemap(GenericSitemap):
    """Use for sitemap entries based on objects that implement get_absolute_url but append a suffix in creating their url"""
    def __init__(self, info_dict, priority=None, changefreq=None):
        GenericSitemap.__init__(self, info_dict, priority=priority, changefreq=changefreq)
        self.suffix = info_dict.get('suffix', '')

    def location(self, obj):
        url = GenericSitemap.location(self, obj)
        return "%s%s" % (url, self.suffix)


sitemaps = {
    'author_detail': GenericSitemap({'queryset':Author.objects,
                                     'date_field':'modified'},
                                    changefreq='monthly',
                                    priority='0.5'),
    'tag_detail': SlugSitemap({'queryset':Tag.objects,
                               'url':'/tag/',
                               'slugfield':'name',
                               'suffix':'/'},
                              changefreq='monthly',
                              priority='0.5'),
    'periodical_detail': GenericSitemap({'queryset':Periodical.objects},
                                        changefreq='monthly',
                                        priority='0.5'),
    'periodicals_read_online': SuffixedSitemap({'queryset':Periodical.objects,
                                                'suffix':'online/'},
                                               changefreq='monthly',
                                               priority='0.5'),
    'periodicals_issue_detail': GenericSitemap({'queryset':Issue.objects.select_related(),
                                                'date_field':'modified'},
                                               changefreq='monthly',
                                               priority='0.6'),
    'periodicals_article_detail': GenericSitemap({'queryset':Article.objects.select_related(),
                                                  'date_field':'modified'},
                                                 changefreq='monthly',
                                                 priority='0.7'),
}
