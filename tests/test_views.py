#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_views
------------

Tests for `django-periodicals` view module.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from periodicals.models import Author, Periodical, Issue, Article


class TestSetup(TestCase):

    def setUp(self):
        author = Author(last_name='Newman',
                        first_name='Alfred',
                        middle_name='E')
        author.save()
        periodical = Periodical(name="Mad Magazine")
        periodical.save()
        issue = Issue(periodical=periodical,
                      volume=1,
                      issue=10)
        issue.save()
        article = Article(issue=issue,
                          series="Editorial",
                          title="What me worry?")
        article.save()
        article.authors.add(author)

        article1 = Article(issue=issue,
                           series="Humor",
                           title="Fun")
        article1.save()
        article1.authors.add(author)


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
