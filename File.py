'''file objects'''

import os
import json

from Pages.ContentPage import ContentPage
from Pages.HomePage import HomePage
from Pages.SpecialPage import SpecialPage
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
        print("FILE ", self.filepath_abs)

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
            self.type = 'special'
        else:
            self.type = self.meta['type']

    def create_page_instance(self):
        type = self.meta['type']

        if type == "home":
            page_inst = HomePage(self)

        elif type == "special":
            page_inst = SpecialPage(self)

        elif type == "imagepage":
            page_inst = ImagePage(self)

        elif type == "article":
            page_inst = ArticlePage(self)

        else:
            page_inst = ContentPage(self)

    def read_content_file(self):
        with open(self.filepath_abs, 'r') as f:
            content = f.read()

        meta_json, body_md = content.split('%%%', 1)

        meta = json.loads(meta_json)

        return meta, body_md
