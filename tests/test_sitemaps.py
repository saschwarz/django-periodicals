#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_sitemaps
------------

Tests for `django-periodicals` sitemaps module.
"""
from django.test import TestCase
from tagging.models import Tag
from periodicals.models import Periodical
from periodicals.sitemaps import (sitemaps, sitemaps_at,
                                  SlugSitemap, SuffixedSitemap)


class TestSitemapsAt(TestCase):

    def test_slug_at_has_root_prepended(self):
        original_url = sitemaps['tag_detail'].url
        new_sitemap = sitemaps_at('/periodicals')
        modified_url = new_sitemap['tag_detail'].url
        self.assertTrue(modified_url.startswith("/periodicals"))
        self.assertTrue(modified_url.endswith(original_url))


class TestSlugSitemap(TestCase):

    def setUp(self):
        self.sitemap = SlugSitemap({'queryset': Tag.objects,
                                    'url': '/tag/',
                                    'slugfield': 'name',
                                    'suffix': '/'},
                                   changefreq='monthly',
                                   priority='0.5')

    def test_location(self):
        tag = Tag(name="meeker")
        self.assertEqual('/tag/meeker/', self.sitemap.location(tag))


class TestSuffixedSitemap(TestCase):

    def setUp(self):
        self.sitemap = SuffixedSitemap({'queryset': Periodical.objects,
                                        'suffix': 'online/'},
                                       changefreq='monthly',
                                       priority='0.5')

    def test_location(self):
        tag = Periodical(slug='clean-run')
        self.assertEqual('/clean-run/online/', self.sitemap.location(tag))
