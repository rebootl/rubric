'''content page object'''

import os
from datetime import datetime

from Pages.ContentFilePage import ContentFilePage
from common import url_encode_str

class ContentPage(ContentFilePage):
    '''Content pages, e.g. an article, an image page aso..'''

    def __init__(self, content_file):
        self.content_file = content_file

        self.create_date_obj()

        page_subdir = url_encode_str(self.content_file.meta['title'])
        out_subdir = os.path.join(self.date_str, page_subdir)

        super().__init__( self.content_file,
                          out_subdir = out_subdir )

        self.site.content_pages.append(self)

    def process(self):
        # sorting and page navigation (prev / index / next)
        self.set_next_page()
        self.set_prev_page()
        self.set_page_nav()        

        self.process_body()

        self.render()
        self.write_out()

        # copy files
        self.copy_files()

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

    def set_next_page(self):
        for num, page in enumerate(self.site.content_pages):
            if page == self:
                next_page_num = num + 1
                if next_page_num + 1 > len(self.site.content_pages):
                    self.next_page = None
                else:
                    self.next_page = self.site.content_pages[num+1]
                    # (debug prints)
                    #print("SELF", self.content_file.meta['title'])
                    #print("NEXT", self.next_page.content_file.meta['title'])

    def set_prev_page(self):
        for num, page in enumerate(self.site.content_pages):
            if page == self:
                prev_page_num = num - 1
                if not prev_page_num < 0:
                    self.prev_page = self.site.content_pages[num-1]
                    #print("PREV", self.prev_page.content_file.meta['title'])
                else:
                    self.prev_page = None

