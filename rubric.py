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
# default page types
#
# - home        (home page, only one)
# - norubric    (other page in root directory, e.g. about) (default)
# - rubricpage  (main rubrics page, one per rubric)
#
# additional page types
#
# - article     (article content page)
# - image       (image content page) --> later split drawing and foto
#
#
#  content                     public
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
