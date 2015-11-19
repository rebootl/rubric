'''page objects'''

# a page consists of a content file,
# plus additional files like embedded images etc.
#
# content file
# ------------
#
# 1) meta information at the beginning using json format
#    e.g.:
#    {
#      "title":  "Welcome Home",
#      "author": "Cem",
#      "date":   "2015-11-16",
#      "type":   "home page",
#      "files":  []
#    }
#    %%%
#
#    delimited by "%%%"
#
# 2) page content in markdown and/or plugin syntax (optional)

import os
from datetime import datetime

from common import pandoc_pipe, write_out

class Page:

    def __init__(self, content_file):
        self.content_file = content_file
        self.subpath = self.content_file.subpath
        self.site = self.content_file.subpath.site

        self.title = content_file.meta['title']
        self.author = content_file.meta['author']
        self.date = content_file.meta['date']
        self.type = content_file.meta['type']
        self.files = content_file.meta['files']

        self.create_date_obj()
        # (sets self.date_obj)

    def create_date_obj(self):
        try:
            self.date_obj = datetime.strptime( self.date,
                                               self.site.config.DATE_FORMAT )
        except ValueError:
            self.date_obj = None

    def process(self):
        pass
        # --> substitute and process plugin content

        # process through pandoc
        self.prepare_pandoc()

        self.page_html = pandoc_pipe( self.content_file.body_md,
                                      self.pandoc_opts )

        # --> back-substitute plugin content

        # write out
        self.write_out()

    def prepare_pandoc(self):

        template_path = os.path.join( self.site.config.TEMPLATE_DIR,
                                      self.template )

        self.pandoc_opts = [ '--to=html5',
                             '--template='+template_path,
                             '--variable=title:'+self.title,
                             '--variable=author:'+self.author,
                             '--variable=date:'+self.date,
                             '--variable=header-title:'+self.header_title ]

    def write_out(self):
        write_out(self.page_html, self.out_filepath)

class HomePage(Page):

    def __init__(self, content_file):
        super().__init__(content_file)

        self.template = "default.html5"

        self.out_path = self.site.config.PUBLISH_DIR
        self.out_filename = "index.html"
        self.out_filepath = os.path.join(self.out_path, self.out_filename)

        self.header_title = ""

class RubricPage(Page):

    def __init__(self, content_file):
        super().__init__(content_file)

        self.template = "default.html5"

        self.out_path = os.path.join( self.site.config.PUBLISH_DIR,
                                      self.title )
        self.out_filename = "index.html"
        self.out_filepath = os.path.join(self.out_path, self.out_filename)

        self.header_title = self.title
