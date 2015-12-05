'''base page object'''

import os

from common import write_out

class Page:

    def __init__( self, site,
                  out_subdir = "",
                  out_filename = "index.html" ):
        self.site = site
        self.site.pages.append(self)

        self.out_subdir = out_subdir
        self.out_filename = out_filename

        if self.out_filename == "index.html":
            self.href = os.path.join('/', self.out_subdir)
        else:
            self.href = os.path.join('/', self.out_subdir, self.out_filename)

        self.out_dir_abs = os.path.join( self.site.config.PUBLISH_DIR,
                                         self.out_subdir )

        self.out_filepath_abs = os.path.join( self.out_dir_abs,
                                              self.out_filename )

        # a dict of variables that will be rendered using self.render()
        self.variables = { 'body': "",
                           'title': "",
                           'author': "",
                           'date': "" }

    def process(self):
        '''Override this in the respective subclasses.'''
        # Usually something like:
        # process page body
        # self.render()
        # self.write_out()
        pass

    def render(self):
        self.page_html = self.site.template.render(self.variables)

    def write_out(self):
        write_out(self.page_html, self.out_filepath_abs)
