'''content file page object'''

import os

from Pages.Page import Page
from common import pandoc_pipe, copy_file
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute

class ContentFilePage(Page):
    '''Page based on a content file.'''

    def __init__( self, content_file,
                  out_subdir = "",
                  out_filename = "index.html" ):
        self.content_file = content_file
        super().__init__(self.content_file.site, out_subdir, out_filename)

        self.type = "contentpage"

        for key in self.site.config.FALLBACK_META_VARIABLES:
            if key not in self.content_file.meta.keys():
                self.variables[key] = self.site.config.FALLBACK_META_VARIABLES[key]
            else:
                self.variables[key] = self.content_file.meta[key]

        self.title = self.variables['title']
        self.author = self.variables['author']

    def process(self):
        self.set_page_nav()
        self.process_body()

        self.render()

        self.write_out()
        self.copy_files()

    def process_body(self):
        # substitute and process plugin content
        self.process_plugin_content()

        # process through pandoc
        pandoc_opts = [ '--to=html5' ]

        self.page_html_subst = pandoc_pipe(self.body_md_subst, pandoc_opts)

        # back-substitute plugin content
        if self.plugin_blocks != []:
            self.variables['body'] = back_substitute( self.page_html_subst,
                                                      self.plugin_blocks )
        else:
            self.variables['body'] = self.page_html_subst

    def process_plugin_content(self):
        # plugin substitution
        self.body_md_subst, \
        self.cdata_blocks = get_cdata(self.content_file.body_md)

        # process the plug-in content
        if self.cdata_blocks != []:
            self.plugin_blocks, \
            self.plugin_pandoc_opts = plugin_cdata_handler( self,
                                                            self.cdata_blocks )
        else:
            self.plugin_blocks = []
            self.plugin_pandoc_opts = []

    def copy_files(self):
        for file in self.content_file.files:
            in_path_abs = os.path.join( self.site.config.CONTENT_DIR,
                                        self.content_file.subpath.subpath,
                                        file )
            if not os.path.isfile(in_path_abs):
                print("Warning: File not found:", file)
                continue
            copy_file(in_path_abs, self.out_dir_abs)
