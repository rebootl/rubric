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

        self.prev_page = None
        self.next_page = None

    def process(self):
        '''Override this in the respective subclasses.'''
        # usually something like:
        # self.process() # (process page body)
        # self.set_page_nav()
        # self.render()
        # self.write_out()
        pass

    def render(self):
        self.page_html = self.site.template.render(self.variables)

    def write_out(self):
        write_out(self.page_html, self.out_filepath_abs)

    def set_page_nav(self):
        self.variables['page_nav'] = True

        if self.prev_page:
            self.variables['prev_href'] = self.prev_page.href
        else:
            self.variables['prev_href'] = self.href
            self.variables['prev_inactive_class'] = "inactive"

        if self.next_page:
            self.variables['next_href'] = self.next_page.href
        else:
            self.variables['next_href'] = self.href
            self.variables['next_inactive_class'] = "inactive"
