#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_models
------------

Tests for `django-periodicals` model module.
"""

from django.test import TestCase
from django.test.utils import override_settings
from periodicals import models


class TestAuthor(TestCase):

    def setUp(self):
        self.author = models.Author(title=models.Author.TITLE_CHOICES[0][1],
                                    first_name="Firstname",
                                    middle_name="Middle",
                                    last_name='Lastname',
                                    postnomial='PhD')

    def test_display_name_last_name_only(self):
        author = models.Author(last_name='Lastname')
        self.assertEqual('Lastname', author.display_name())

    def test_display_name_fully_populated(self):
        self.assertEqual('Lastname, Firstname Middle PhD',
                         self.author.display_name())

    @override_settings(PERIODICALS_AUTHOR_FORMAT='%(last_name)s - %(first_name)s %(middle_name)s %(postnomial)s')
    def test_display_name_fully_populated_format_settings_override(self):
        self.assertEqual('Lastname - Firstname Middle PhD',
                         self.author.display_name())

    def test_save_with_auto_generated_slug(self):
        self.author.save()
        self.assertEqual('lastname-firstname-middle-phd',
                         self.author.slug)

    def test_save_with_user_slug(self):
        self.author.slug = "userProvidedSlug"
        self.author.save()
        self.assertEqual("userProvidedSlug", self.author.slug)

    @override_settings(PERIODICALS_AUTHOR_SLUG_FORMAT='%(last_name)s %(first_name)s')
    def test_save_with_auto_generated_slug_with_format_settings_override(self):
        self.author.save()
        self.assertEqual('lastname-firstname',
                         self.author.slug)


class TestPeriodical(TestCase):

    def setUp(self):
        self.periodical = models.Periodical(name="Issue Name",
                                            country="USA")

    def test_display_name(self):
        self.assertEqual('Issue Name',
                         self.periodical.display_name())

    @override_settings(PERIODICALS_PERIODICAL_FORMAT='%(name)s - %(country)s')
    def test_display_name_format_settings_override(self):
        self.assertEqual('Issue Name - USA',
                         self.periodical.display_name())

    def test_save_with_auto_generated_slug(self):
        self.periodical.save()
        self.assertEqual("issue-name",
                         self.periodical.slug)

    def test_save_with_user_slug(self):
        self.periodical.slug = "userProvidedSlug"
        self.periodical.save()
        self.assertEqual("userProvidedSlug", self.periodical.slug)

    @override_settings(PERIODICALS_PERIODICAL_SLUG_FORMAT='%(name)s %(country)s')
    def test_save_with_auto_generated_slug_with_format_settings_override(self):
        self.periodical.save()
        self.assertEqual("issue-name-usa",
                         self.periodical.slug)


class TestIssue(TestCase):

    def setUp(self):
        periodical = models.Periodical(name="Issue Name",
                                       country="USA")
        periodical.save()
        self.issue = models.Issue(periodical=periodical,
                                  volume=1,
                                  issue=10)

    def test_display_name(self):
        self.assertEqual('Vol. 1 No. 10',
                         self.issue.display_name())

    @override_settings(PERIODICALS_ISSUE_FORMAT='%(volume)s - %(issue)s')
    def test_display_name_format_settings_override(self):
        self.assertEqual('1 - 10',
                         self.issue.display_name())

    def test_save_with_auto_generated_slug(self):
        self.issue.save()
        self.assertEqual("1-10",
                         self.issue.slug)

    def test_save_with_user_slug(self):
        self.issue.slug = "userProvidedSlug"
        self.issue.save()
        self.assertEqual("userProvidedSlug", self.issue.slug)

    @override_settings(PERIODICALS_ISSUE_SLUG_FORMAT='%(issue)s %(volume)s')
    def test_save_with_auto_generated_slug_with_format_settings_override(self):
        self.issue.save()
        self.assertEqual("10-1",
                         self.issue.slug)

    def test_save_with_title_uses_title_as_slug(self):
        self.issue.title = 'my fave issue'
        self.issue.save()
        self.assertEqual('my-fave-issue', self.issue.slug)

    def test_save_with_existing_slug_does_not_change_slug(self):
        self.issue.title = 'my least fave issue'
        self.issue.slug = 'a-user-defined-slug'
        self.issue.save()
        self.assertEqual('a-user-defined-slug', self.issue.slug)

    def test_save_with_existing_id_does_not_change_slug(self):
        self.issue.save()
        self.assertTrue(self.issue.id)
        self.assertEqual('1-10', self.issue.slug)
        self.issue.title = 'changed title'
        self.issue.save()
        self.assertEqual('1-10', self.issue.slug)

    def test_display_name_is_title_for_titled_issue(self):
        self.issue.title = 'my fave issue'
        self.assertEqual('my fave issue', self.issue.display_name())

    def test_display_name_is_issue_format_for_untitled_issue(self):
        self.issue.title = ''
        self.assertEqual('Vol. 1 No. 10', self.issue.display_name())

    @override_settings(PERIODICALS_ISSUE_FORMAT='Volume: %(volume)s')
    def test_display_name_is_configured_issue_format_for_untitled_issue(self):
        self.issue.title = ''
        self.assertEqual('Volume: 1', self.issue.display_name())


class TestArticle(TestCase):

    def setUp(self):
        periodical = models.Periodical(name="Issue Name",
                                       country="USA")
        periodical.save()
        self.periodical = periodical
        issue = models.Issue(periodical=periodical,
                             volume=1,
                             issue=10)
        issue.save()
        self.issue = issue
        self.article = models.Article(issue=issue)

    def test_slug_is_generated_from_title(self):
        self.article.title = "This is the article title"
        self.article.save()
        self.assertEqual("this-is-the-article-title", self.article.slug)

    def test_slug_is_generated_from_title_and_made_globally_unique(self):
        self.article.title = "This is the article title"
        self.article.save()
        issue = models.Issue(periodical=self.periodical,
                             volume=1,
                             issue=11)
        issue.save()
        article = models.Article(issue=issue,
                                 title="This is the article title")
        article.save()
        self.assertEqual("this-is-the-article-title-2", article.slug)
