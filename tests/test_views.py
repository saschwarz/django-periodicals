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


class TestAuthorViews(TestCase):

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
                          title="What me worry?")
        article.save()
        article.authors.add(author)
        article.save()

    def test_authors_list(self):
        resp = self.client.get(reverse('periodicals_authors_list'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/author_list.html')
        authors = resp.context['author_list']
        self.assertEqual(1, len(authors))
        self.assertEqual(1, authors[0].pk)
        self.assertEqual(1, authors[0].articles__count)

    def test_author_detail(self):
        resp = self.client.get(reverse('periodicals_author_detail', 
                                       kwargs={'slug': 'newman-alfred-e'}))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'periodicals/author_detail.html')
        author = resp.context['author']
        self.assertEqual(1, author.pk)
        article_list = resp.context['article_list']
        self.assertEqual(1, len(article_list))
