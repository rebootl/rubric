'''main site objects'''

from Subpath import Subpath


class Site:

    def __init__(self):
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
