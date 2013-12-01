from django.views.generic import ArchiveIndexView, DetailView, ListView, TemplateView, YearArchiveView
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import mail_managers
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site

# from tagging.views import tagged_object_list
# from recaptcha_utils.fields import ReCaptchaField
from .models import Author, Periodical, Issue, Article, LinkItem


class AuthorList(ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.annotate(Count('articles')).\
        order_by("last_name", "first_name")
    template_name = 'periodicals/author_list.html'


class AuthorDetail(DetailView):
    model = Author
    context_object_name = 'author'
    slug_url_kwarg = 'author_slug'
    template_name = 'periodicals/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        author = context['author']
        context['article_list'] = author.articles.all().\
            select_related().order_by('-issue__pub_date')
        return context


class SeriesList(ListView):
    model = Article
    context_object_name = 'series_list'
    template_name = 'periodicals/series_list.html'

    def get_queryset(self):
        self.periodical = get_object_or_404(Periodical,
                                       slug=self.kwargs['periodical_slug'])
        return Article.objects.filter(issue__periodical=self.periodical).\
            order_by('series').values('series').annotate(series_count=Count('series'))

    def get_context_data(self, **kwargs):
        context = super(SeriesList, self).get_context_data(**kwargs)
        context['periodical'] = self.periodical
        return context


class SeriesDetail(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'periodicals/series_detail.html'

    def get_queryset(self):
        self.periodical = get_object_or_404(Periodical,
                                            slug=self.kwargs['periodical_slug'])
        self.series = self.kwargs['series']
        return Article.objects.filter(issue__periodical=self.periodical).\
            filter(series=self.series).\
            select_related().order_by('-issue__pub_date')

    def get_context_data(self, **kwargs):
        context = super(SeriesDetail, self).get_context_data(**kwargs)
        context['periodical'] = self.periodical
        context['series'] = self.series
        return context


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


class PeriodicalList(ListView):
    model = Periodical
    template_name = 'periodicals/periodical_list.html'


class PeriodicalDetail(ArchiveIndexView):
    model = Issue
    date_field = 'pub_date'
    allow_future = True
    template_name = 'periodicals/periodical_detail.html'
    slug_url_kwarg = 'periodical_slug'

    def get_queryset(self):
        self.periodical_slug = self.kwargs['periodical_slug']
        qs = super(PeriodicalDetail, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super(PeriodicalDetail, self).get_context_data(**kwargs)
        periodical = get_object_or_404(Periodical, slug=self.periodical_slug)
        context['periodical'] = periodical
        return context


class IssueYear(YearArchiveView):
    queryset = Issue.objects.all()
    date_field = 'pub_date'
    make_object_list = True
    allow_future = False
    template_name = 'periodicals/issue_year.html'

    def get_queryset(self):
        periodical_slug = self.kwargs['periodical_slug']
        periodical = get_object_or_404(Periodical, slug=periodical_slug)
        self.periodical = periodical
        qs = super(IssueYear, self).get_queryset().filter(periodical=periodical)
        return qs

    def get_context_data(self, **kwargs):
        context = super(IssueYear, self).get_context_data(**kwargs)
        context['periodical'] = self.periodical
        return context


class IssueDetail(TemplateView):
    # issue_slug is only unique per month so can't use
    # regular DetailView
    template_name = 'periodicals/issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        periodical_slug = kwargs['periodical_slug']
        periodical = get_object_or_404(Periodical,
                                       slug=periodical_slug)
        issue = get_object_or_404(Issue,
                                  periodical=periodical,
                                  slug=kwargs['issue_slug'])
        try:
            next_month = Issue.objects.filter(periodical=periodical).\
                filter(pub_date__gt=issue.pub_date).order_by('pub_date')[0:1].get()
        except ObjectDoesNotExist:
            next_month = None

        try:
            previous_month = Issue.objects.filter(periodical=periodical).\
                filter(pub_date__lt=issue.pub_date).order_by('-pub_date')[0:1].get()
        except ObjectDoesNotExist:
            previous_month = None

        context['issue'] = issue
        context['periodical'] = periodical
        context['previous_month'] = previous_month
        context['next_month'] = next_month
        return context


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'article_slug'
    template_name = 'periodicals/article_detail.html'

    def get_queryset(self):
        periodical_slug = self.kwargs['periodical_slug']
        self.periodical = get_object_or_404(Periodical,
                                            slug=periodical_slug)
        issue_slug = self.kwargs['issue_slug']
        self.issue = get_object_or_404(Issue,
                                       periodical=self.periodical,
                                       slug=issue_slug)
        return super(ArticleDetail, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = context['article']
        next_article = previous_article = None
        if article.page:
            try:
                next_article = Article.objects.filter(issue=self.issue).\
                    filter(page__gt=article.page).order_by('page')[0:1].get()
            except ObjectDoesNotExist:
                next_article = None
            try:
                previous_article = Article.objects.filter(issue=self.issue).\
                    filter(page__lt=article.page).order_by('-page')[0:1].get()
            except ObjectDoesNotExist:
                previous_article = None
        context['periodical'] = self.periodical
        context['issue'] = self.issue
        context['previous_article'] = previous_article
        context['next_article'] = next_article
        return context


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
#     return add_link(request, 
#                     article,
#                     admin_url=urlresolvers.reverse('admin:periodicals_article_change', 
#                                                    args=(article.id,)))


# def add_issue_link(request, periodical_slug, slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     issue = get_object_or_404(Issue, slug=slug, periodical=periodical)
#     return add_link(request,
#                     issue,
#                     admin_url=urlresolvers.reverse('admin:periodicals_issue_change', 
#                                                    args=(issue.id,)))


# def links(request, periodical_slug):
#     periodical = get_object_or_404(Periodical, slug=periodical_slug)
#     # Load all the links and their related Issues/Article instances efficiently
# #    article_type = ContentType.objects.get_for_model(Article)
#     articles = Article.objects.filter(issue__periodical=periodical).filter(links__status='A').distinct().select_related().order_by('-issue__pub_date')
# #    issue_type = ContentType.objects.get_for_model(Issue)
#     issues = Issue.objects.filter(periodical=periodical).filter(links__status='A').distinct().select_related().order_by('-pub_date')

#     return render_to_response('periodicals/links.html',
#                               {'articles': articles,
#                                'issues': issues,
#                                'periodical': periodical,
#                                },
#                               context_instance=RequestContext(request)
#                               )


# class LinkItemForm(forms.Form):
#     title = forms.CharField()
#     url = forms.URLField()
# #     recaptcha = ReCaptchaField()


# def add_link(request, object,
#              form_class=LinkItemForm,
#              template_name='periodicals/link_add.html',
#              success_url='/periodicals/links/added/',
#              admin_url=""):
#     if request.method == 'POST':
#         form = form_class(data=request.POST)
#         if form.is_valid():
#             object.links.create(status='S',
#                                 url=form.cleaned_data['url'],
#                                 title=form.cleaned_data['title'])
#             email_body = "Link added to: http://%s%s admin: http://%s%s" % (
#                 Site.objects.get_current().domain,
#                 object.get_absolute_url(),
#                 Site.objects.get_current().domain,
#                 admin_url)
#             mail_managers("New Link Added", email_body)
#             return HttpResponseRedirect(success_url)
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
