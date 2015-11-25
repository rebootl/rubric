'''subpath object'''

import os

from File import ContentFile
from Page import Page, HomePage, RubricPage, NoRubricPage
from ContentPage import ContentPage
from ImagePage import ImagePage
from Rubric import Rubric

class Subpath:

    def __init__(self, content, subpath=""):
        print("SUBPATH", subpath)
        self.content = content
        self.content.subpaths.append(self)
        self.site = content.site
        self.subpath = subpath

        self.path_abs = os.path.join(self.site.config.CONTENT_DIR, subpath)

        self.content_files = []
        self.subdirs = []

        self.load_content()

    def load_content(self):

        # get dir content
        dir_content = os.listdir(self.path_abs)

        subdirs = []
        # get content files
        for filename in dir_content:
            if filename.endswith(self.site.config.PAGE_EXT):
                file = ContentFile(self, filename)
                self.content_files.append(file)

            elif os.path.isdir( os.path.join( self.path_abs, filename) ):
                subdirs.append(filename)

        # create page instances
        for file in self.content_files:
            self.create_page_instance(file)

        # recurse
        for subdir in subdirs:
            subpath_inst = Subpath(self.content, subdir)
            self.subdirs.append(subpath_inst)

    def create_page_instance(self, file):
        type = file.meta['type']

        if type == "home":
            page_inst = HomePage(file)

        elif type == "norubric":
            page_inst = NoRubricPage(file)

        elif type == "rubricpage":
            rubric = self.new_rubric(file.rubric_name)
            page_inst = RubricPage(file, rubric)

        elif type == "image":
            rubric = self.new_rubric(file.rubric_name)
            page_inst = ImagePage(file, rubric)

        else:
            rubric = self.new_rubric(file.rubric_name)
            page_inst = ContentPage(file, rubric)

    def new_rubric(self, rubric_name):
        rubric = self.site.get_rubric_by_name(rubric_name)
        if not rubric:
            rubric = Rubric(self.site, rubric_name)

        return rubric
