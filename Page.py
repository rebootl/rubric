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
#      "type":   "home",
#      "files":  []
#    }
#    %%%
#
#    delimited by "%%%"
#
# 2) page content in markdown and/or plugin syntax (optional)

import os
from datetime import datetime

from common import pandoc_pipe, write_out, copy_file
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute

class Page:

    # for processing currently needed are:
    # .site
    # .variables        (dict of pandoc variables)
    # .template         (pandoc template name)
    # .header_title     (header title, for my use usually the Rubric name)
    # .body_md
    # .out_path
    # .out_filename
    # .files            (list of associated files) --> not yet used

    def __init__(self, content_file):
        self.content_file = content_file
        self.subpath = self.content_file.subpath
        self.site = self.content_file.subpath.site
        self.site.pages.append(self)

        self.meta = self.content_file.meta
        self.variables = {}
        self.body_md = self.content_file.body_md

        self.title = self.meta['title']
        self.author = self.meta['author']
        self.date = self.meta['date']
        self.type = self.content_file.type
        self.files = self.content_file.files
        #self.rubric_name = self.content_file.rubric_name

        self.create_date_obj()
        # (sets self.date_obj)

        self.template = "default.html5"
        self.add_stylesheets = []

    def preprocess(self):
        self.out_dir_abs = os.path.join( self.site.config.PUBLISH_DIR,
                                         self.out_dir )
        self.out_filepath_abs = os.path.join( self.out_dir_abs,
                                              self.out_filename )

    def create_date_obj(self):
        try:
            self.date_obj = datetime.strptime( self.date,
                                               self.site.config.DATE_FORMAT )
        except ValueError:
            self.date_obj = None

    def process(self):
        # substitute and process plugin content
        self.process_plugin_content()
        # sets:
        # - self.body_md_subst
        # - self.cdata_blocks
        # - self.plugin_blocks
        # - self.plugin_pandoc_opts

        # process through pandoc
        self.prepare_pandoc()

        self.page_html_subst = pandoc_pipe( self.body_md_subst,
                                            self.pandoc_opts )

        # back-substitute plugin content
        if self.plugin_blocks != []:
            self.page_html = back_substitute( self.page_html_subst,
                                              self.plugin_blocks )
        else:
            self.page_html = self.page_html_subst

        # write out
        self.write_out()

        # copy files
        self.copy_files()

    def process_plugin_content(self):
        # plugin substitution
        self.body_md_subst, \
        self.cdata_blocks = get_cdata(self.body_md)

        # process the plug-in content
        if self.cdata_blocks != []:
            self.plugin_blocks, \
            self.plugin_pandoc_opts = plugin_cdata_handler( self,
                                                            self.cdata_blocks )
        else:
            self.plugin_blocks = []
            self.plugin_pandoc_opts = []

    def prepare_pandoc(self):

        template_path = os.path.join( self.site.config.TEMPLATE_DIR,
                                      self.template )

        self.pandoc_opts = [ '--to=html5',
                             '--template='+template_path ]

        # add default meta variables
        for key in self.site.config.DEFAULT_META_DICT:
            self.pandoc_opts.append( '--variable=' + key
                                                   + ':'
                                                   + self.meta[key] )

        # add variables
        self.variables['header-title'] = self.header_title
        self.variables['rubric-list'] = self.site.rubric_list.menu

        for key in self.variables.keys():
            self.pandoc_opts.append( '--variable=' + key
                                                   + ':'
                                                   + self.variables[key] )

        # additional stylesheets
        if 'stylesheet' in self.meta.keys():
            self.add_stylesheets.append(self.meta['stylesheet'])
        for add_stylesheet in self.add_stylesheets:
            self.pandoc_opts.append('--variable=add-stylesheet:' + add_stylesheet)

    def write_out(self):
        #out_filepath = os.path.join( self.site.config.PUBLISH_DIR,
        #                             self.out_dir,
        #                             self.out_filename )
        write_out(self.page_html, self.out_filepath_abs)

    def copy_files(self):
        for file in self.files:
            in_path_abs = os.path.join( self.site.config.CONTENT_DIR,
                                        self.subpath.subpath,
                                        file )
            if not os.path.isfile(in_path_abs):
                print("Warning: File not found:", file)
                continue
            copy_file(in_path_abs, self.out_dir_abs)

class HomePage(Page):

    def __init__(self, content_file):
        super().__init__(content_file)

        self.site.homepage = self

        self.out_filename = "index.html"
        self.out_dir = ""

        self.header_title = ""

        self.preprocess()

class RubricPage(Page):

    def __init__(self, content_file, rubric):
        super().__init__(content_file)
        self.rubric = rubric
        self.rubric.rubric_page = self
        # (one for now, could be several later)
        # (don't add here for now)
        #rubric.pages.append(page_inst)

        self.out_filename = "index.html"
        self.out_dir = self.rubric.name

        self.header_title = self.rubric.name

        self.preprocess()

class NoRubricPage(Page):

    def __init__(self, content_file):
        super().__init__(content_file)

        # evtl. change to "url encoded" later
        self.out_filename = os.path.splitext(content_file.name)[0] + '.html'
        self.out_dir = ""

        self.header_title = self.title

        self.preprocess()

# derived objects in separate files
#
# - ContentPage
# - ImagePage
