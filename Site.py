'''main objects'''

from jinja2 import Environment, FileSystemLoader

from Subpath import Subpath
#from Menu import RubricList
from Pages.ListingPage import ListingByDatePage
from common import sort_pages

class Config:

    def __init__(self, CONTENT_DIR, PUBLISH_DIR, TEMPLATE_DIR,
                    TEMPLATE_NAME, PAGE_EXT):

        self.CONTENT_DIR = CONTENT_DIR
        self.PUBLISH_DIR = PUBLISH_DIR
        self.TEMPLATE_DIR = TEMPLATE_DIR
        self.TEMPLATE_NAME = TEMPLATE_NAME
        self.PAGE_EXT = PAGE_EXT

        # date format for content files,
        # format acc. to Python datetime.datetime.strptime,
        # one of these can be used
        self.DATE_FORMAT = "%Y-%m-%d"
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M"

        self.FALLBACK_META_VARIABLES = {
            'title': "NO TITLE SET",
            'author': "NO AUTHOR SET",
            'date': "NO DATE SET"
        }

class Site:

    def __init__( self, CONTENT_DIR, PUBLISH_DIR, TEMPLATE_DIR,
                  TEMPLATE_NAME = "html5.html",
                  PAGE_EXT = ".page" ):

        self.config = Config( CONTENT_DIR,
                              PUBLISH_DIR,
                              TEMPLATE_DIR,
                              TEMPLATE_NAME,
                              PAGE_EXT )

        # all rubrics, will be filled by Rubric instances,
        # wich are in turn generated as needed
        #self.rubrics = []
        # all pages, will be filled by Page instances
        self.pages = []
        self.content_pages = []

        # load jinja2 template
        self.load_template()

        # load content
        self.content = Content(self)

        # --> sort stuff
        # ..
        self.content_pages = sort_pages(self.content_pages)
        #for rubric in self.rubrics:
        #    rubric.sort()

        # generate rubric list
        #self.rubric_list = RubricList(self)

        # generate listing page
        listing_inst = ListingByDatePage(self)

        # process pages
        for page in self.pages:
            page.process()

    def load_template(self):
        env = Environment(loader=FileSystemLoader(self.config.TEMPLATE_DIR))

        self.template = env.get_template(self.config.TEMPLATE_NAME)

    #def get_rubric_by_name(self, rubric_name):
    #    for rubric in self.rubrics:
    #        if rubric_name == rubric.name:
    #            return rubric
    #    return None


class Content:

    def __init__(self, site):
        self.site = site

        self.subpaths = []
        subpath_inst = Subpath(self)
