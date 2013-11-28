from django.views.generic import ListView
#from django.views.generic.date_based import archive_index, archive_year, archive_month
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import mail_managers
from django.core import urlresolvers
from django.contrib.sites.models import Site
# from tagging.views import tagged_object_list
from .models import Author, Periodical, Issue, Article, LinkItem
#from recaptcha_utils.fields import ReCaptchaField


class AuthorList(ListView):
    model = Author
    queryset = Author.objects.annotate(Count('articles')).order_by("last_name", "first_name")
    context_object_name = 'author_list'
    template_name = 'periodicals/author_list.html'


class AuthorDetail(ListView):
    template_name = 'periodicals/author_detail.html'
    context_object_name = 'article_list'
    paginate_by = 20

    def get_queryset(self):
        self.author = get_object_or_404(Author, slug=self.kwargs['slug'])
        return self.author.articles.all().select_related().order_by('-issue__pub_date')

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(*kwargs)
        context['author'] = self.author
        return context

# def series_list(request, periodical_slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     return object_list(request,
#                        # get_absolute_url() needs related Periodical and Issue
#                        queryset=Article.objects.filter(issue__periodical=periodical).order_by('series').values('series').annotate(series_count=Count('series')),
#                        template_name='periodicals/series_list.html',
#                        extra_context={'periodical':periodical}
#                        )


# def series_detail(request, periodical_slug, series_slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     return object_list(request,
#                        # get_absolute_url() needs related Periodical and Issue
#                        queryset=Article.objects.filter(series=series_slug).select_related().order_by('-issue__pub_date'),
#                        template_name='periodicals/series_detail.html',
#                        paginate_by=20,
#                        extra_context={'periodical':periodical,
#                                       'series':series_slug}
#                        )


# # when related_tags=True can't yet pass a QuerySet:
# # http://code.google.com/p/django-tagging/issues/detail?id=179
# def tag_detail(request, tag):
#     tag = tag.replace('-', ' ')
#     return tagged_object_list(request,
#                               queryset_or_model=Article.objects.order_by('-issue__pub_date').select_related().all(),
#                               tag=tag,
#                               template_name='periodicals/article_tag_detail.html',
# #                              related_tags=True,
# #                              related_tag_counts=True,
#                               paginate_by=20)


# # Costly since Issue and Periodical instances are loaded for each tagged Article
# # def tag_detail(request, tag):
# #     tag = tag.replace('-', ' ')
# #     return tagged_object_list(request,
# #                               queryset_or_model=Article,
# #                               tag=tag,
# #                               template_name='periodicals/article_tag_detail.html',
# #                               related_tags=True,
# #                               related_tag_counts=True,
# #                               paginate_by=20)

# def periodical_detail(request, slug):
#     periodical = get_object_or_404(Periodical, slug=slug)
#     series_query_set = Article.objects.filter(issue__periodical=periodical).order_by('series').values('series').distinct()[:10]
#     return archive_index(request,
#                          queryset=periodical.issue_set.order_by('pub_date'),
#                          date_field='pub_date',
#                          num_latest=None,
#                          template_name='periodicals/periodical_detail.html',
#                          extra_context={'periodical': periodical,
#                                         'series_list': series_query_set},
#                         allow_future=True)


# def issue_year(request, periodical_slug, year):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     next = int(year)+1
#     next_year = Issue.objects.filter(periodical=periodical).filter(pub_date__year=next).count() and next or None
#     previous = int(year)-1
#     previous_year = Issue.objects.filter(periodical=periodical).filter(pub_date__year=previous).count() and previous or None
#     return archive_year(request,
#                         year,
#                         Issue.objects.filter(periodical=periodical).all().select_related().order_by("pub_date"),
#                         'pub_date',
#                         template_name='periodicals/issue_year.html',
#                         extra_context={'periodical': periodical,
#                                        'next_year': next_year,
#                                        'previous_year': previous_year},
#                         make_object_list=True,
#                         allow_future=True)


# def issue_detail(request, periodical_slug, slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     issue = get_object_or_404(Issue, slug=slug, periodical=periodical)
#     next_month = Issue.objects.filter(periodical=periodical).filter(pub_date__gt=issue.pub_date).order_by('pub_date')
#     if next_month:
#         next_month = next_month[0]
#     previous_month = Issue.objects.filter(periodical=periodical).filter(pub_date__lt=issue.pub_date).order_by('-pub_date')
#     if previous_month:
#         previous_month = previous_month[0]
#     return object_list(request,
#                        # Still querying for each author individually
#                        queryset=Article.objects.filter(issue=issue).select_related().order_by('page'),
#                        template_name='periodicals/issue_detail.html',
#                        extra_context={'issue': issue,
#                                       'periodical': periodical,
#                                       'next_month': next_month,
#                                       'previous_month': previous_month
#                                       })


# def article_detail(request, periodical_slug, issue_slug, slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     issue = get_object_or_404(Issue, slug=issue_slug, periodical=periodical)
#     article = get_object_or_404(Article, slug=slug, issue=issue)
#     if article.page:
#         next_article = Article.objects.filter(issue=issue).filter(page__gt=article.page).order_by('page')
#         if next_article:
#             next_article = next_article[0]
#         previous_article = Article.objects.filter(issue=issue).filter(page__lt=article.page).order_by('-page')
#         if previous_article:
#             previous_article = previous_article[0]
#     else:
#         next_article = previous_article = None
#     return render_to_response('periodicals/article_detail.html',
#                               {'article' : article,
#                                'issue': issue,
#                                'periodical': periodical,
#                                'next_article': next_article,
#                                'previous_article': previous_article
#                                },
#                               context_instance=RequestContext(request)
#                               )


# def read_online(request, periodical_slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     return render_to_response('periodicals/read_online.html',
#                               {'articles' : Article.objects.exclude(read_online__exact='').select_related().order_by('-issue__pub_date'),
#                                'issues': Issue.objects.exclude(read_online__exact='').select_related().order_by('-pub_date'),
#                                'periodical': periodical,
#                                },
#                               context_instance=RequestContext(request)
#                               )


# def add_article_link(request, periodical_slug, issue_slug, slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     issue = get_object_or_404(Issue, slug=issue_slug, periodical=periodical)
#     article = get_object_or_404(Article, slug=slug, issue=issue)
#     return add_link(request, article,
#                     admin_url=urlresolvers.reverse('admin:periodicals_article_change', args=(article.id,)))


# def add_issue_link(request, periodical_slug, slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     issue = get_object_or_404(Issue, slug=slug, periodical=periodical)
#     return add_link(request, issue,
#                     admin_url=urlresolvers.reverse('admin:periodicals_issue_change', args=(issue.id,)))


# def links(request, periodical_slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     # Load all the links and their related Issues/Article instances efficiently
#     article_type = ContentType.objects.get_for_model(Article)
#     articles = Article.objects.filter(issue__periodical=periodical).filter(links__status='A').distinct().select_related().order_by('-issue__pub_date')
#     issue_type = ContentType.objects.get_for_model(Issue)
#     issues = Issue.objects.filter(periodical=periodical).filter(links__status='A').distinct().select_related().order_by('-pub_date')

#     return render_to_response('periodicals/links.html',
#                               {'articles' : articles,
#                                'issues': issues,
#                                'periodical': periodical,
#                                },
#                               context_instance=RequestContext(request)
#                               )


# class LinkItemForm(forms.Form):
#     title = forms.CharField()
#     url = forms.URLField()
#     recaptcha = ReCaptchaField()


# def add_link(request, object,
#              form_class=LinkItemForm,
#              template_name='periodicals/link_add.html',
#              success_url='/periodicals/links/added/',
#              admin_url=""):
#     if request.method == 'POST':
#         form = form_class(data=request.POST)
#         if form.is_valid():
#              link = object.links.create(status='S',
#                                         url=form.cleaned_data['url'],
#                                         title=form.cleaned_data['title'])
#              email_body = "Link added to: http://%s%s admin: http://%s%s" % (
#                  Site.objects.get_current().domain,
#                  object.get_absolute_url(),
#                  Site.objects.get_current().domain,
#                  admin_url)
#              mail_managers("New Link Added", email_body)
#              return HttpResponseRedirect(success_url)
#     else:
#         form = form_class()
#     return render_to_response(template_name,
#                               {'form': form,
#                                'object': object,
#                                'object_class': object.__class__.__name__,
#                                },
#                               context_instance=RequestContext(request))


# def add_link_success(request, template_name="periodicals/link_success.html"):
#     return render_to_response(template_name,
#                               context_instance=RequestContext(request))
