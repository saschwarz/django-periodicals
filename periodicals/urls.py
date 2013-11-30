from django.contrib import admin
from django.conf.urls import patterns, url
from .views import (AuthorList, AuthorDetail,
                    PeriodicalList, PeriodicalDetail,
                    SeriesList, SeriesDetail,
                    IssueYear, IssueDetail, ArticleDetail)


urlpatterns = patterns('',
                       # not in sitemap
                       url(r'^authors/$',
                           AuthorList.as_view(),
                           name='periodicals_authors_list',
                           ),

                       url(r'^authors/(?P<author_slug>[-\w]+)/$',
                           AuthorDetail.as_view(),
                           name='periodicals_author_detail'
                           ),

                       # url(r'^tags/$',
                       #     TemplateView.as_view(template_name='periodicals/tags.html'),
                       #     name='periodicals_tags',
                       #     ),

                       # url(r'^tag/(?P<tag>[^/]+)/$',
                       #     'periodicals.views.tag_detail',
                       #     name='periodicals_article_tag_detail'
                       #     ),

                       # # success for adding a link - don't include in sitemap
                       # url(r'^links/added/$',
                       #     'periodicals.views.add_link_success',
                       #     name='periodicals_add_link_success'
                       #     ),

                       # # add a link to an article - don't include in sitemap
                       # url(r'^links/(?P<periodical_slug>[-\w]+)/(?P<issue_slug>[-\w]+)/(?P<link_slug>[-\w]+)/$',
                       #     'periodicals.views.add_article_link',
                       #     name='periodicals_add_article_link'
                       #     ),

                       # # add a link to an issue - don't include in sitemap
                       # url(r'^links/(?P<periodical_slug>[-\w]+)/(?P<link_slug>[-\w]+)/$',
                       #     'periodicals.views.add_issue_link',
                       #     name='periodicals_add_issue_link'
                       #     ),

                       # # Page showing all periodical Issues and Articles with external links
                       # url(r'^links/(?P<periodical_slug>[-\w]+)/$',
                       #     'periodicals.views.links',
                       #     name='periodicals_links'
                       #     ),

                       # periodical detail including list of periodical's years
                       url(r'^(?P<periodical_slug>[-\w]+)/$',
                           PeriodicalDetail.as_view(),
                           name='periodicals_periodical_detail'
                           ),

                       # # list of periodical's issues and articles viewable online
                       # url(r'^(?P<periodical_slug>[-\w]+)/online/$',
                       #     'periodicals.views.read_online',
                       #     name='periodicals_read_online'
                       #     ),

                       # list of periodical's issues for a year - not in sitemap
                       url(r'^(?P<periodical_slug>[-\w]+)/(?P<year>\d{4})/$',
                           IssueYear.as_view(),
                           name='periodicals_issue_year'
                           ),

                       # list of periodical's series - not in sitemap
                       url(r'^(?P<periodical_slug>[-\w]+)/series/$',
                           SeriesList.as_view(),
                           name='periodicals_series_list'
                           ),

                       # list of articles in a series - not in sitemap
                       url(r'^(?P<periodical_slug>[-\w]+)/series/(?P<series>.+)/$',
                           SeriesDetail.as_view(),
                           name='periodicals_series_detail'
                           ),

                       # one periodical issue
                       url(r'^(?P<periodical_slug>[-\w]+)/(?P<issue_slug>[-\w]+)/$',
                           IssueDetail.as_view(),
                           name='periodicals_issue_detail'
                           ),

                       # one article
                       url(r'^(?P<periodical_slug>[-\w]+)/(?P<issue_slug>[-\w]+)/(?P<article_slug>[-\w]+)/$',
                           ArticleDetail.as_view(),
                           name='periodicals_article_detail'
                           ),

                       # list of periodicals - not in sitemap
                       url(r'',
                           PeriodicalList.as_view(),
                           name='periodicals_list'
                           ),
                       )


# Haystack search support is optional
try:
    from haystack.views import SearchView
    from haystack.query import SearchQuerySet

    # query results with most recent publication date first
    sqs = SearchQuerySet().order_by('-pub_date')

    urlpatterns += patterns('', 
                            # not in sitemap
                            url(r'^search/',
                                SearchView(load_all=False,
                                           searchqueryset=sqs,
                                           ),
                                name='haystack_search',
                                )
                            )
except:
    pass


admin.autodiscover()
