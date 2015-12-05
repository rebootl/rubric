'''file objects'''

import os
import json

from Rubric import Rubric
from Pages.ContentPage import ContentPage
from Pages.HomePage import HomePage
from Pages.RubricPage import RubricPage
from Pages.NoRubricPage import NoRubricPage
from Pages.ArticlePage import ArticlePage
from Pages.ImagePage import ImagePage

class File:

    def __init__(self, subpath, name):
        self.subpath = subpath
        self.site = self.subpath.site
        self.name = name

        self.filepath_abs = os.path.join( subpath.site.config.CONTENT_DIR,
                                          subpath.subpath,
                                          name )
        print("File: ", self.filepath_abs)

class ContentFile(File):

    def __init__(self, subpath, name):
        super().__init__(subpath, name)

        self.meta, self.body_md = self.read_content_file()

        self.set_defaults()
        self.create_page_instance()

    def set_defaults(self):
        '''set some sane defaults'''

        if 'files' not in self.meta.keys():
            self.files = []
        else:
            self.files = self.meta['files']

        if 'type' not in self.meta.keys():
            self.type = 'norubric'
        else:
            self.type = self.meta['type']

        if 'rubric' not in self.meta.keys():
            if self.type == 'home':
                pass
            elif self.type == 'norubric':
                pass
            else:
                quit( "Error: {} type needs a rubric in header: {}".format(
                    self.type,
                    self.filepath_abs
                ) )
        else:
            self.rubric_name = self.meta['rubric']

    def create_page_instance(self):
        type = self.meta['type']

        if type == "home":
            page_inst = HomePage(self)

        elif type == "norubric":
            page_inst = NoRubricPage(self)

        elif type == "rubricpage":
            rubric = self.new_rubric()
            page_inst = RubricPage(self, rubric)

        elif type == "imagepage":
            rubric = self.new_rubric()
            page_inst = ImagePage(self, rubric)

        elif type == "article":
            rubric = self.new_rubric()
            page_inst = ArticlePage(self, rubric)

        else:
            rubric = self.new_rubric()
            page_inst = ContentPage(self, rubric)

    def new_rubric(self):
        rubric = self.site.get_rubric_by_name(self.rubric_name)
        if not rubric:
            rubric = Rubric(self.site, self.rubric_name)

        return rubric

    def read_content_file(self):
        with open(self.filepath_abs, 'r') as f:
            content = f.read()

        meta_json, body_md = content.split('%%%', 1)

        meta = json.loads(meta_json)

        return meta, body_md
