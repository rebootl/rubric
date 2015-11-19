'''main site objects'''

from Subpath import Subpath


class Config:

    def __init__(self, CONTENT_DIR, PUBLISH_DIR, TEMPLATE_DIR, PAGE_EXT):
        self.CONTENT_DIR = CONTENT_DIR
        self.PUBLISH_DIR = PUBLISH_DIR
        self.TEMPLATE_DIR = TEMPLATE_DIR
        self.PAGE_EXT = PAGE_EXT

        # date format (acc. to Python datetime.datetime.strptime)
        self.DATE_FORMAT = "%Y-%m-%d"


class Site:

    def __init__(self, CONTENT_DIR, PUBLISH_DIR, TEMPLATE_DIR,
                  PAGE_EXT=".page" ):

        self.config = Config( CONTENT_DIR,
                              PUBLISH_DIR,
                              TEMPLATE_DIR,
                              PAGE_EXT )

        self.rubrics = []
        self.pages_all = []
        self.pages = []

        # load content
        self.content = Content(self)

        # process pages
        for page in self.pages_all:
            page.process()

    def get_rubric_by_name(self, rubric_name):
        for rubric in self.rubrics:
            if rubric_name == rubric.name:
                return rubric
        return None


class Content:

    def __init__(self, site):
        self.site = site

        self.subpaths = []
        subpath_inst = Subpath(self)
