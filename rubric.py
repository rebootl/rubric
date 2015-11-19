#!/usr/bin/python
'''rubric - an emphasis on content'''

# want that cool shit, ey

# an "inner" representation of the website shall be created
# by page object instances
#
#
# "rubrics" are categories, e.g. 'Drawings', 'Articles', 'Fotos'
#
#
# page types
#
# - home          (home page, only one)
# - rubric        (main rubrics page, one per rubric)
# - <rubric name> (content page)
# - norubric      (other, e.g. about page)
#
#
#  content                     public
#
#   home ------------------> index.html
#
#   norubric --------------> <title-url-compat>.html (e.g. about page)
#
#   rubric ----------------> <rubric name>/index.html
#
#   <content page> --------> <rubric name>/<date>/<title-url-compat>.html
#                                                /<content> (images etc.)
#
#                            rubric.html (list of rubrics, generated)
#

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

    for subpath in site.content.subpaths:
        print(subpath.subpath)

    for page in site.pages:
        print(page.title)

        #for page in subpath.pages:
        #    print(page.title)
        #    print(page.date)

    print(site.homepage.title)

    for rubric in site.rubrics:
        print(rubric.name)

script()
