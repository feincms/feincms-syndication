from __future__ import unicode_literals

import feedparser
import socket

from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


socket.setdefaulttimeout(5)  # 5 seconds


class FeedContent(models.Model):
    url = models.URLField(
        _('Feed URL'),
        help_text=_(
            'Insert any RSS URL,'
            ' e.g. https://www.djangoproject.com/rss/weblog/'),
    )
    items = models.IntegerField(_('items'), default=10)

    class Meta:
        abstract = True
        verbose_name = _('RSS feed')
        verbose_name_plural = _('RSS feeds')

    @classmethod
    def initialize_type(cls, TYPE_CHOICES):
        cls.add_to_class(
            'type',
            models.CharField(
                _('type'),
                max_length=20,
                choices=TYPE_CHOICES,
                default=TYPE_CHOICES[0][0],
            ))

    def cache_key(self):
        return '%s:%s' % (
            self.__class__.__name__,
            self.pk,
        )

    def save(self, *args, **kwargs):
        super(FeedContent, self).save(*args, **kwargs)
        cache.delete(self.cache_key())
    save.alerts_data = True

    def delete(self, *args, **kwargs):
        super(FeedContent, self).delete(*args, **kwargs)
        cache.delete(self.cache_key())
    delete.alerts_data = True

    def render(self, **kwargs):
        html = cache.get(self.cache_key())

        if html is not None:
            return html

        feed = feedparser.parse(self.url)
        entries = feed['entries'][:self.items]

        html = render_to_string(
            [
                'content/feincms_syndication/%s.html' % self.type,
                'content/feincms_syndication/default.html',
            ],
            {
                'content': self,
                'entries': entries,
            }, context_instance=kwargs.get('context'))

        cache.set(self.cache_key(), html, timeout=3600)
        return html
