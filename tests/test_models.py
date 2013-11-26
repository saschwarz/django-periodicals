#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-periodicals
------------

Tests for `django-periodicals` modules module.
"""

import os
import shutil
from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings
from django.template.defaultfilters import slugify
from periodicals import models


class TestAuthor(TestCase):

    def setUp(self):
        self.author = models.Author(title=models.Author.TITLE_CHOICES[0][1],
                                    first_name="Firstname",
                                    middle_name="Middle",
                                    last_name='Lastname',
                                    postnomial='PhD')

    def test_get_name_display_last_name_only(self):
        author = models.Author(last_name='Lastname')
        self.assertEqual('Lastname', author.get_name_display())

    def test_get_name_display_fully_populated(self):
        self.assertEqual('Lastname, Firstname Middle PhD',
                         self.author.get_name_display())

    @override_settings(PERIODICALS_AUTHOR_FORMAT='%(last_name)s - %(first_name)s %(middle_name)s %(postnomial)s')
    def test_get_name_display_fully_populated_format_settings_override(self):
        self.assertEqual('Lastname - Firstname Middle PhD',
                         self.author.get_name_display())

    def test_save_with_auto_generated_slug(self):
        self.author.save()
        self.assertEqual(slugify(settings.PERIODICALS_AUTHOR_SLUG_FORMAT % self.author._instanceFields()),
                         self.author.slug)

    def test_save_with_user_slug(self):
        self.author.slug = "userProvidedSlug"
        self.author.save()
        self.assertEqual("userProvidedSlug", self.author.slug)

    @override_settings(PERIODICALS_AUTHOR_SLUG_FORMAT='%(last_name)s %(first_name)s')
    def test_save_with_auto_generated_slug_with_format_settings_override(self):
        self.author.save()
        self.assertEqual(slugify(settings.PERIODICALS_AUTHOR_SLUG_FORMAT % self.author._instanceFields()),
                         self.author.slug)

    def tearDown(self):
        pass
