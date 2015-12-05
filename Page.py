'''page objects'''

import os
from datetime import datetime

from common import pandoc_pipe, write_out, copy_file, url_encode_str
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute
import tags

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

        # some stuff

        # ...

    def process(self):
        self.process_body()

        # add menu
        self.variables['rubric_list'] = self.site.rubric_list.menu

        self.render()
        self.write_out()

        # copy files
        self.copy_files()

    def process_body(self):
        # substitute and process plugin content
        self.process_plugin_content()
        # sets:
        # - self.body_md_subst
        # - self.cdata_blocks
        # - self.plugin_blocks
        # - self.plugin_pandoc_opts

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

class HomePage(ContentFilePage):
    '''The home page, /index.html.'''

    def __init__(self, content_file):
        self.content_file = content_file
        super().__init__(self.content_file)

        self.type = "homepage"

class RubricPage(ContentFilePage):
    '''Main page of a rubric, e.g. Articles.'''

    def __init__(self, content_file, rubric):
        self.content_file = content_file
        self.rubric = rubric
        super().__init__( self.content_file,
                          out_subdir = self.rubric.name )

        self.type = "rubricpage"
        self.rubric.rubric_page = self

        self.variables['header_title'] = self.rubric.name

class NoRubricPage(ContentFilePage):
    '''Other pages not associated with a rubrig, e.g. About, Links etc..'''

    def __init__(self, content_file):
        self.content_file = content_file
        out_filename = os.path.splitext(content_file.name)[0] + '.html'
        # (evtl. change to "url encoded" later)

        super().__init__( self.content_file,
                          out_filename = out_filename )

        self.type = 'norubricpage'

        self.variables['header_title'] = self.variables['title']

class ContentPage(ContentFilePage):
    '''Content pages, e.g. an article, an image page aso..'''

    def __init__(self, content_file, rubric):
        self.content_file = content_file
        self.rubric = rubric

        self.create_date_obj()

        out_filename = url_encode_str( self.content_file.meta['title'] ) \
                        + '.html'
        out_subdir = os.path.join( self.rubric.name, self.date_str )

        super().__init__( self.content_file,
                          out_subdir = out_subdir,
                          out_filename = out_filename )

        self.rubric.pages.append(self)

        self.variables['header_title'] = self.rubric.name

    def create_date_obj(self):
        try:
            self.date_obj = datetime.strptime(
                self.content_file.meta['date'],
                self.content_file.site.config.DATE_FORMAT
            )
            self.date_str = self.date_obj.strftime("%Y-%m-%d")
        except ValueError:
            try:
                self.date_obj = datetime.strptime(
                    self.content_file.meta['date'],
                    self.content_file.site.config.DATETIME_FORMAT
                )
                self.date_str = self.date_obj.strftime("%Y-%m-%d")
            except ValueError:
                print("Warning: Erroneous date/datetime:", self.content_file.filepath_abs)
                self.date_obj = None
                self.date_str = "ERRONEOUS_DATE"

    def sort(self):
        self.next_page()
        self.prev_page()
        self.set_page_nav()

    def next_page(self):
        for num, page in enumerate(self.rubric.pages):
            if page == self:
                next_page_num = num + 1
                if next_page_num + 1 > len(self.rubric.pages):
                    self.next_page = None
                else:
                    self.next_page = self.rubric.pages[num+1]
                    print("SELF", self.content_file.meta['title'])
                    print("NEXT", self.next_page.content_file.meta['title'])

    def prev_page(self):
        for num, page in enumerate(self.rubric.pages):
            if page == self:
                prev_page_num = num - 1
                if not prev_page_num < 0:
                    self.prev_page = self.rubric.pages[num-1]
                    print("PREV", self.prev_page.content_file.meta['title'])
                else:
                    self.prev_page = None

    def set_page_nav(self):
        self.variables['page_nav'] = True

        self.variables['index_href'] = os.path.join('/', self.rubric.name)

        if self.prev_page:
            self.variables['prev_href'] = self.prev_page.href
            #self.variables['prev_inactive_class'] = ""
        else:
            self.variables['prev_href'] = self.href
            self.variables['prev_inactive_class'] = "inactive"

        if self.next_page:
            self.variables['next_href'] = self.next_page.href
        else:
            self.variables['next_href'] = self.href
            self.variables['next_inactive_class'] = "inactive"

class ArticlePage(ContentPage):

    def __init__(self, content_file, rubric):
        super().__init__(content_file, rubric)

        self.type = 'article'
        self.variables['article_title'] = True

# derived objects in separate files
#
# - ImagePage
