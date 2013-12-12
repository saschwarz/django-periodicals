#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_templatetags
------------

Tests for `django-periodicals` periodical_tags module.
"""
from datetime import datetime
from django.test import TestCase
from periodicals import models
from periodicals.templatetags.periodicals_tags import (
    periodical_copyright,
    ArticleCountNode)


class TestPeriodicalCopyright(TestCase):

    def test_without_autoescape(self):
        periodical = models.Periodical(publisher=">ABC Press<",
                                       website="http://example.com")
        self.assertEqual('Titles, descriptions and images are copyright <a href="http://example.com">>ABC Press<</a> and are used with permission.', 
                         periodical_copyright(periodical))

    def test_with_autoescape(self):
        periodical = models.Periodical(publisher=">ABC Press<",
                                       website="http://example.com")
        self.assertEqual('Titles, descriptions and images are copyright <a href="http://example.com">&gt;ABC Press&lt;</a> and are used with permission.', 
                         periodical_copyright(periodical, autoescape=True))


class TestArticleCount(TestCase):

    def test_count_is_one_when_one_article(self):
        periodical = models.Periodical(name="Periodical Name",
                                       country="USA")
        periodical.save()
        issue = models.Issue(periodical=periodical,
                             volume=1,
                             issue=10,
                             pub_date=datetime(2013, 11, 1))
        issue.save()
        article = models.Article(issue=issue)
        article.save()
        tag = ArticleCountNode()
        self.assertEqual("1", tag.render(None))

    def test_count_is_zero_when_no_articles(self):
        tag = ArticleCountNode()
        self.assertEqual("0", tag.render(None))
