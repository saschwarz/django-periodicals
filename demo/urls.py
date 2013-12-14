from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView

from periodicals.sitemaps import sitemaps_at

urlpatterns = \
    patterns('',
             # use admin to add periodicals, authors, issues, etc.
             url(r'^admin/', include(admin.site.urls)),
             # assuming periodicals is a sub application
             # in your project
             url(r'^periodicals/', include('periodicals.urls')),
             # optional sitemap support
             (r'^sitemap.xml$',
              'django.contrib.sitemaps.views.sitemap',
              {'sitemaps': sitemaps_at('/periodicals')}),
             # the root splash screen
             url(r'^$',
                 TemplateView.as_view(template_name='index.html'),
                 name='index',
                 ),
             )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
