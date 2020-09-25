#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jon Steven Dal Williams'
SITENAME = "Dal's Portfolio"
SITEURL = 'https://dalwilliams.info'

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Twitter' 'twitter.com/dendrondal'),
          ('LinkedIn', 'https://www.linkedin.com/in/dal-williams/'),
          ('GitHub', 'github.com/dendrondal'))
M_SOCIAL_TWITTER_SITE = '@dendrondal' 
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
STATIC_PATHS = ['images']


#Theme stuff
THEME = 'm.css/pelican-theme'
THEME_STATIC_DIR = 'static'
DIRECT_TEMPLATES = ['index']

M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
               '/static/m-dark.css']
M_THEME_COLOR = '#353535'

PLUGIN_PATHS = ['m.css/plugins']
PLUGINS = ['m.htmlsanity', 'm.code', 'm.components']

M_FAVICON = ('images/favicon.ico', 'image/x-ico')
M_SITE_LOGO = 'images/tree.jpg'
# Navbar
M_LINKS_NAVBAR1 = [('About', 'pages/about-me.html', 'about', []),
                   ('Resume',
                    'https://github.com/dendrondal/Portfolio/raw/pelican_migration/content/pages/Williams_Dal_Resume.pdf', 'resume', []),
                    ('GitHub', 'https://github.com/dendrondal', '', []),
                    ('LinkedIn', 'https://linkedin.com/in/dal-williams', '', []),
                    ('Twitter', 'https://twitter.com/dendrondal', '', [])]
