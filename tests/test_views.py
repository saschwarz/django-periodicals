#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_views
------------

Tests for `django-periodicals` view module.
"""
import os
import urlparse
from datetime import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from periodicals.models import Author, Periodical, Issue, Article

os.environ['RECAPTCHA_TESTING'] = 'True'

class TestSetup(TestCase):

    def setUp(self):
        author = Author(last_name='Newman',
                        first_name='Alfred',
                        middle_name='E')
        author.save()
        self.author = author
        periodical = Periodical(name="Mad Magazine")
        periodical.save()
        self.periodical = periodical
        issue0 = Issue(periodical=periodical,
                       volume=1,
                       issue=9,
                       pub_date=datetime(2011, 9, 1)
                       )
        issue0.save()
        self.issue0 = issue0
        issue1 = Issue(periodical=periodical,
                       volume=1,
                       issue=10,
                       pub_date=datetime(2011, 10, 1)
                       )
        issue1.save()
        self.issue1 = issue1
        issue2 = Issue(periodical=periodical,
                       volume=1,
                       issue=11,
                       pub_date=datetime(2011, 11, 1)
                       )
        issue2.save()
        self.issue2 = issue2
        article = Article(issue=issue1,
                          series="Editorial",
                          title="What me worry?")
        article.save()
        article.authors.add(author)
        self.article = article
        article1 = Article(issue=issue1,
                           series="Humor",
                           title="Fun")
        article1.save()
        article1.authors.add(author)
        self.article1 = article1


class TestAuthorViews(TestSetup):

    def test_authors_list(self):
        resp = self.client.get(reverse('periodicals_authors_list'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/author_list.html')
        authors = resp.context['author_list']
        self.assertEqual(1, len(authors))
        self.assertEqual(1, authors[0].pk)
        self.assertEqual(2, authors[0].articles__count)

    def test_author_detail(self):
        resp = self.client.get(reverse('periodicals_author_detail',
                                       kwargs={'author_slug': 'newman-alfred-e'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/author_detail.html')
        author = resp.context['author']
        self.assertEqual(1, author.pk)
        article_list = resp.context['article_list']
        self.assertEqual(2, len(article_list))


class TestSeriesViews(TestSetup):

    def test_series_list(self):
        resp = self.client.get(reverse('periodicals_series_list',
                                       kwargs={'periodical_slug': 'mad-magazine'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/series_list.html')
        self.assertTemplateUsed(resp, 'periodicals/periodicals_base.html')
        self.assertTemplateUsed(resp, 'periodicals/base.html')
        series = resp.context['series_list']
        self.assertEqual(2, len(series))
        self.assertEqual('Editorial', series[0]['series'])
        self.assertEqual(1, series[0]['series_count'])
        self.assertEqual('Humor', series[1]['series'])
        self.assertEqual(1, series[1]['series_count'])

    def test_series_detail(self):
        resp = self.client.get(reverse('periodicals_series_detail',
                                       kwargs={'periodical_slug': 'mad-magazine',
                                               'series': 'Editorial'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/series_detail.html')
        series = resp.context['series']
        self.assertEqual('Editorial', series)
        periodical = resp.context['periodical']
        self.assertEqual(1, periodical.pk)
        article_list = resp.context['article_list']
        self.assertEqual(1, len(article_list))
        self.assertTrue(isinstance(article_list[0], Article))


class TestPeriodicalViews(TestSetup):

    def test_periodical_detail(self):
        resp = self.client.get(reverse('periodicals_periodical_detail',
                                       kwargs={'periodical_slug': 'mad-magazine'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/periodical_detail.html')
        periodical = resp.context['periodical']
        self.assertEqual(1, periodical.id)
        issue_list = resp.context['date_list']
        self.assertEqual(1, len(issue_list))


class TestIssueViews(TestSetup):

    def test_issue_detail(self):
        periodical = Periodical(name="One Issue")
        periodical.save()

        single_issue = Issue(periodical=periodical,
                             volume=2,
                             issue=1,
                             pub_date=datetime(2012, 1, 1)
                             )
        single_issue.save()
        resp = self.client.get(
            reverse('periodicals_issue_detail',
                    kwargs={'periodical_slug': periodical.slug,
                            'issue_slug': single_issue.slug}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/issue_detail.html')
        issue = resp.context['issue']
        self.assertEqual(single_issue, issue)
        periodical = resp.context['periodical']
        self.assertEqual(periodical, periodical)
        previous_month = resp.context['previous_month']
        self.assertEqual(None, previous_month)
        next_month = resp.context['next_month']
        self.assertEqual(None, next_month)

    def test_issue_detail_with_previous_and_next_issues(self):
        resp = self.client.get(reverse('periodicals_issue_detail',
                                       kwargs={'periodical_slug': 'mad-magazine',
                                               'issue_slug': '1-10'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/issue_detail.html')
        issue = resp.context['issue']
        self.assertEqual(self.issue1, issue)
        periodical = resp.context['periodical']
        self.assertEqual(self.periodical, periodical)
        previous_month = resp.context['previous_month']
        self.assertEqual(self.issue0, previous_month)
        next_month = resp.context['next_month']
        self.assertEqual(self.issue2, next_month)

    def test_save_with_duplicate_volume_issue_on_same_date_gives_different_slug(self):
        dup_issue1 = Issue(periodical=self.periodical,
                           volume=1,
                           issue=10,
                           pub_date=datetime.strptime('2011-10-01', '%Y-%m-%d')
                           )
        self.assertRaises(IntegrityError, dup_issue1.save)
        self.assertEqual(dup_issue1.slug, self.issue1.slug)


class TestIssueYearView(TestSetup):

    def test_issue_year(self):
        resp = self.client.get(reverse('periodicals_issue_year',
                                       kwargs={'periodical_slug': 'mad-magazine',
                                               'year': 2011,
                                               }))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/issue_year.html')
        periodical = resp.context['periodical']
        self.assertEqual(self.periodical, periodical)
        issue_list = resp.context['date_list']
        self.assertEqual(3, len(issue_list))
        year = resp.context['year']
        self.assertEqual('2011', year.strftime('%Y'))
        next_year = resp.context['next_year']
        self.assertEqual(None, next_year)
        previous_year = resp.context['previous_year']
        self.assertEqual(None, previous_year)

    def test_with_same_issues_in_multiple_periodicals(self):
        periodical = Periodical(name="Crazy Cat")
        periodical.save()
        issue10 = Issue(periodical=periodical,
                        volume=0,
                        issue=10,
                        pub_date=datetime.strptime('2010-01-01', '%Y-%m-%d')
                        )
        issue10.save()
        issue0 = Issue(periodical=periodical,
                       volume=1,
                       issue=10,
                       pub_date=datetime.strptime('2011-10-01', '%Y-%m-%d')
                       )
        issue0.save()
        issue1 = Issue(periodical=periodical,
                       volume=1,
                       issue=11,
                       pub_date=datetime.strptime('2011-11-01', '%Y-%m-%d')
                       )
        issue1.save()
        issue2 = Issue(periodical=periodical,
                       volume=2,
                       issue=1,
                       pub_date=datetime.strptime('2012-01-01', '%Y-%m-%d')
                       )
        issue2.save()
        url = reverse('periodicals_issue_year',
                                       kwargs={'periodical_slug': 'crazy-cat',
                                               'year': '2011',
                                               })
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        issue_list = resp.context['date_list']
        self.assertEqual(2, len(issue_list))
        year = resp.context['year']
        self.assertEqual('2011', year.strftime('%Y'))
        next_year = resp.context['next_year']
        self.assertEqual('2012', next_year.strftime('%Y'))
        previous_year = resp.context['previous_year']
        self.assertEqual('2010', previous_year.strftime('%Y'))
        

class TestArticleDetailView(TestSetup):

    def test_article_detail_one_article(self):
        single_periodical = Periodical(name="One Issue")
        single_periodical.save()

        single_issue = Issue(periodical=single_periodical,
                             volume=2,
                             issue=1,
                             pub_date=datetime(2012, 1, 1)
                             )
        single_issue.save()
        article = Article(issue=single_issue,
                          series="Humor",
                          title="Fun Alone")
        article.save()
        article.authors.add(self.author)

        resp = self.client.get(
            reverse('periodicals_article_detail',
                    kwargs={'periodical_slug': single_periodical.slug,
                            'issue_slug': single_issue.slug,
                            'article_slug': article.slug
                            }))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/article_detail.html')
        periodical = resp.context['periodical']
        self.assertEqual(single_periodical, periodical)
        issue = resp.context['issue']
        self.assertEqual(single_issue, issue)
        next_article = resp.context['next_article']
        self.assertEqual(None, next_article)
        previous_article = resp.context['previous_article']
        self.assertEqual(None, previous_article)
        
    def test_article_detail_one_previous_and_one_next_article(self):
        self.article1.page = 8
        self.article1.save()
        self.article.page = 10
        self.article.save()
        article2 = Article(issue=self.issue1,
                           series="Humor",
                           title="Fun 2",
                           page=11)
        article2.save()

        resp = self.client.get(
            reverse('periodicals_article_detail',
                    kwargs={'periodical_slug': 'mad-magazine',
                            'issue_slug': self.issue1.slug,
                            'article_slug': self.article.slug
                            }))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/article_detail.html')
        periodical = resp.context['periodical']
        self.assertEqual(self.periodical, periodical)
        issue = resp.context['issue']
        self.assertEqual(self.issue1, issue)
        next_article = resp.context['next_article']
        self.assertEqual(article2, next_article)
        previous_article = resp.context['previous_article']
        self.assertEqual(self.article1, previous_article)


class TestReadOnline(TestSetup):

    def test_read_online(self):
        self.issue1.read_online = 'a url'
        self.issue1.save()
        self.article1.read_online = 'a url'
        self.article1.save()

        resp = self.client.get(
            reverse('periodicals_read_online',
                    kwargs={'periodical_slug': self.periodical.slug,
                            }))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/read_online.html')
        periodical = resp.context['periodical']
        self.assertEqual(self.periodical, periodical)
        issues = resp.context['issues']
        self.assertEqual(1, len(issues))
        self.assertEqual(self.issue1, issues[0])
        articles = resp.context['articles']
        self.assertEqual(1, len(articles))
        self.assertEqual(self.article1, articles[0])


class TestTagViews(TestSetup):

    def setUp(self):
        super(TestTagViews, self).setUp()
        self.article.tags = 'humor adult-content'
        self.article.save()
        self.article1.tags = 'humor'
        self.article1.save()

    def test_tags(self):
        resp = self.client.get(reverse('periodicals_tags'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/tags.html')
        self.assertTemplateUsed(resp, 'periodicals/base.html')
        self.assertTrue('adult-content' in resp.content)
        self.assertTrue('humor' in resp.content)

    def test_tag_detail(self):
        resp = self.client.get(reverse('periodicals_article_tag_detail',
                                       kwargs={'tag': 'adult-content'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/article_tag_detail.html')
        self.assertTemplateUsed(resp, 'periodicals/base.html')
        self.assertTrue('adult-content' in resp.content)
        self.assertTrue('humor' in resp.content)


class TestLinkViews(TestSetup):

    def setUp(self):
        super(TestLinkViews, self).setUp()
        self.article.links.create(status='A',
                                  url="http://example.com/",
                                  title="Example Site")
        self.article.save()

    def test_links(self):
        links = self.article.active_links()
        self.assertEqual(1, len(links))
        resp = self.client.get(reverse('periodicals_links',
                                       kwargs={'periodical_slug': self.periodical.slug}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/links.html')
        self.assertTemplateUsed(resp, 'periodicals/periodicals_base.html')
        self.assertTemplateUsed(resp, 'periodicals/base.html')
        self.assertEqual(self.article, resp.context['articles'][0])
        self.assertEqual(0, len(resp.context['issues']))
        self.assertEqual(self.periodical, resp.context['periodical'])
        self.assertTrue(links[0].title in resp.content)
        self.assertTrue(links[0].url in resp.content)

    def test_add_issue_link(self):
        resp = self.client.post(reverse('periodicals_add_issue_link',
                                        kwargs={'periodical_slug': self.periodical.slug,
                                                'issue_slug': self.issue0.slug}),
                                {'title': 'link title',
                                 'url': 'http://example.com',
                                 'recaptcha_response_field': "PASSED"})
        self.assertEqual(resp.status_code, 302)
        # redirects to success page 
        redirect_url = urlparse.urlsplit(resp['Location']).path
        dest = reverse('periodicals_add_link_success')
        self.assertTrue(redirect_url.endswith(dest))
        self.assertTrue(2, len(self.issue0.links.all()))

    def test_add_article_link(self):
        resp = self.client.post(reverse('periodicals_add_article_link',
                                        kwargs={'periodical_slug': self.periodical.slug,
                                                'issue_slug': self.issue1.slug,
                                                'article_slug': self.article.slug}),
                                {'title': 'link title',
                                 'url': 'http://example.com',
                                 'recaptcha_response_field': "PASSED"})
        self.assertEqual(resp.status_code, 302)
        # redirects to success page 
        redirect_url = urlparse.urlsplit(resp['Location']).path
        dest = reverse('periodicals_add_link_success')
        self.assertTrue(redirect_url.endswith(dest))
        # did link get created?
        self.assertTrue(2, len(self.article.links.all()))

class TestSearch(TestSetup):

    def test_search_get(self):
        resp = self.client.get(reverse('haystack_search'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('', resp.context['query'])

    def test_search_query(self):
        self.article.description = 'having some fun now'
        self.article.save()
        resp = self.client.get(reverse('haystack_search'),
                               {'q': 'having'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('having', resp.context['query'])
