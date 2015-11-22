'''main site objects'''

from Subpath import Subpath
from Menu import RubricList

class Config:

    def __init__(self, CONTENT_DIR, PUBLISH_DIR, TEMPLATE_DIR, PAGE_EXT):
        self.CONTENT_DIR = CONTENT_DIR
        self.PUBLISH_DIR = PUBLISH_DIR
        self.TEMPLATE_DIR = TEMPLATE_DIR
        self.PAGE_EXT = PAGE_EXT

        # date format (acc. to Python datetime.datetime.strptime)
        self.DATE_FORMAT = "%Y-%m-%d"

        # default meta information
        self.DEFAULT_META_DICT = {
            'title': "Warning: No title set in content file.",
            'author': "Warning: No author set in content file.",
            'date': "Warning: No date set in content file." 
        }


class Site:

    def __init__(self, CONTENT_DIR, PUBLISH_DIR, TEMPLATE_DIR,
                  PAGE_EXT=".page" ):

        self.config = Config( CONTENT_DIR,
                              PUBLISH_DIR,
                              TEMPLATE_DIR,
                              PAGE_EXT )

        self.rubrics = []
        self.pages = []

        # load content
        self.content = Content(self)

        # generate rubric list
        self.rubric_list = RubricList(self)

        # process pages
        for page in self.pages:
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
