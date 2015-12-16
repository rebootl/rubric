'''home page object'''

from Pages.ContentFilePage import ContentFilePage, Page

class HomePage(ContentFilePage):
    '''The home page, /index.html.'''

    def __init__(self, content_file):
        self.content_file = content_file
        super().__init__(self.content_file)

        self.type = "homepage"

class LatestHomePage(Page):

    def __init__(self, site):
        super().__init__(site)

    def process(self):

        self.latest_page = self.site.content_pages[-1]

        self.page_html = self.latest_page.page_html

        self.write_out()
        self.copy_latest_page_files()
        self.remove_previous_page_files()

    def copy_latest_page_files(self):
        for file in self.latest_page.content_file.files:
            in_path_abs = os.path.join( self.site.config.CONTENT_DIR,
                                        self.latest_page.content_file.subpath.subpath,
                                        file )
            if not os.path.isfile(in_path_abs):
                print("Warning: File not found:", file)
                continue
            copy_file(in_path_abs, self.out_dir_abs)

    def remove_previous_page_files(self):
        previous_page = self.site.content_pages[-2]

        for file in previous_page.content_file.files:
            filepath_abs = os.path.join( self.out_dir_abs,
                                         file )
            if os.path.isfile(filepath_abs):
                print("Removing previous file:", filepath_abs)
                #os.remove(filepath_abs)
