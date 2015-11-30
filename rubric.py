#!/usr/bin/python
'''rubric - an emphasis on content'''

#   want that cool shit, ey"
#
#   an "inner" representation of the website shall be created
#   by page object instances
#
#
#   "rubrics" are categories, e.g. 'Drawings', 'Articles', 'Fotos'
#
#
#
# The entire website is simply created based on content files.
# The structure of these files is not important, they could even
# be distributed over several different directories. (currently only
# one directory is implemented)
#
# The website structure is automatically created, therefor several
# types of content files / pages are supported.
#
# Currently these are:
#
# - home        (home page, only one)
# - norubric    (other page in root directory, e.g. about) (default)
# - rubricpage  (main rubrics page, one per rubric)
#
# - article     (article content page)
# - image       (image content page) --> later split drawing and foto
#
#
#  content type              publish destination
#
#   home ------------------> index.html
#
#   norubric --------------> <filename>.html
#                            --> later use: <title-url-compat>.html
#
#   rubricpage ------------> <rubric name>/index.html
#
#   <add page type> -------> <rubric name>/<date>/<title-url-compat>.html
#                                                /<content> (images etc.)
#
#                            menu-fallback.html (list of rubrics, generated)
#
# content files
# -------------
#
# a content file contains:
#
# 1) meta information at the beginning, using json format
#    e.g.:
#    {
#      "title":  "Welcome Home",
#      "author": "Cem",
#      "date":   "2015-11-16",
#      "type":   "home",
#      "files":  []
#    }
#    %%%
#
#    delimited by "%%%"
#
# 2) page content in markdown and/or plugin syntax (optional)
#
#
# Usage:

from Site import Site

def script():

    site = Site( CONTENT_DIR = "/home/cem/website_rubric/content/",
                 PUBLISH_DIR = "/home/cem/website_rubric/public/",
                 TEMPLATE_DIR = "/home/cem/website_rubric/templates/" )
    # this already loads content from the content directory
    # set in config.CONTENT_DIR
    #
    # Objects   Instance Lists
    #
    #  Site     .subpaths
    #           .homepage
    #  Subpath  .content_files
    #           .pages
    #

#    for subpath in site.content.subpaths:
#        print(subpath.subpath)

#    for page in site.pages:
#        print(page.variables['title'])

        #for page in subpath.pages:
        #    print(page.title)
        #    print(page.date)

#    print(site.homepage.title)

#    for rubric in site.rubrics:
#        print(rubric.name)

script()
