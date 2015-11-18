'''main site objects'''

from Subpath import Subpath


class Config:

    def __init__(self, CONTENT_DIR, TEMPLATE_DIR, PAGE_EXT):
        self.CONTENT_DIR = CONTENT_DIR
        self.TEMPLATE_DIR = TEMPLATE_DIR
        self.PAGE_EXT = PAGE_EXT


class Site:

    def __init__(self, CONTENT_DIR, TEMPLATE_DIR, PAGE_EXT=".page"):
        self.config = Config(CONTENT_DIR, TEMPLATE_DIR, PAGE_EXT)

        self.rubrics = []
        self.pages = []

        self.content = Content(self)

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
