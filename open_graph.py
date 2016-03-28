# -*- coding: utf-8 -*- #
"""
Open Graph
==========

This plugin adds Open Graph Protocol tags to articles.

Use like this in your template:

.. code-block:: jinja2

    {% for tag in article.ogtags %}
        <meta property="{{tag[0]}}" content="{{tag[1]|striptags|e}}" />
    {% endfor %}

"""
from __future__ import unicode_literals

import os.path

from pelican import contents
from pelican import signals
from pelican.utils import strftime, path_to_url

def tag_article(instance):
    if not isinstance(instance, contents.Article):
        return

    ogtags = [('og:title', instance.title),
              ('og:type', 'article')]

    image = instance.metadata.get('og_image', '')
    if image:
        ogtags.append(('og:image', image))

    url = os.path.join(instance.settings.get('SITEURL', ''), instance.url)
    ogtags.append(('og:url', url))

    ogtags.append(('og:description', instance.metadata.get('og_description',
                                                           instance.metadata.get('summary',
                                                                                 instance.summary))))

    default_locale = instance.settings.get('LOCALE', [])
    if default_locale:
        default_locale = default_locale[0]
    else:
        default_locale = ''
    ogtags.append(('og:locale', instance.metadata.get('og_locale', default_locale)))

    ogtags.append(('og:site_name', instance.settings.get('SITENAME', '')))

    ogtags.append(('article:published_time', strftime(instance.date, "%Y-%m-%d")))
    
    if hasattr(instance, 'modified'):
        ogtags.append(('article:modified_time', strftime(instance.modified, "%Y-%m-%d")))

    author_fb_profiles = instance.settings.get('AUTHOR_FB_ID', {})
    if len(author_fb_profiles) > 0:
        for author in instance.authors:
            if author.name in author_fb_profiles:
                ogtags.append(('article:author', author_fb_profiles[author.name]))

    ogtags.append(('article:section', instance.category.name))

    try:
        for tag in instance.tags:
            ogtags.append(('article:tag', tag.name))
    except AttributeError:
            pass

    instance.ogtags = ogtags


def register():
    signals.content_object_init.connect(tag_article)

