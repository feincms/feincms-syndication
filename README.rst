===================
feincms-syndication
===================

``feincms-syndication`` can be used to add RSS feed output to your site.

Steps:

1. Install ``feincms-syndication`` into your virtualenv.
2. Add ``'feincms_syndication'`` to ``INSTALLED_APPS``.
3. Create the content type::

    from feincms.module.page.models import Page
    from feincms_syndication.contents import FeedContent

    Page.create_content_type(
        FeedContent,
        TYPE_CHOICES=(('default', _('Default')),))

The content is looking for templates in the following order in the folder
``content/feincms_syndication/``:

 1. Type + ``.html``
 2. ``default.html``

