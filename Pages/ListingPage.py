'''listing (by date) page object'''

import os

from Pages.Page import Page
from common import sort_pages

class ListingPage(Page):

    def __init__( self, site, out_subdir="",
                  out_filename="listing.html" ):
        super().__init__(site, out_subdir, out_filename)

    def process(self):
        self.set_page_nav()
        self.gen_listing_variables()
        self.render()
        self.write_out()

    def gen_body(self):
        pass

class ListingByDatePage(ListingPage):

    def __init__(self, site):
        super().__init__( site, "",
                          "indexbydate.html" )

        self.variables['title'] = "Index"

    def gen_listing_variables(self):
        # get a copy of all content pages
        content_pages_unsorted = self.site.content_pages.copy()

        # drop pages that have bad date
        for page in content_pages_unsorted:
            if not page.date_obj:
                print( "Warning: Page has bad date, dropping from index:",
                       page.content_file.filepath_abs )
                content_pages_unsorted.remove(page)

        # sort by date
        content_pages = reversed(sort_pages(content_pages_unsorted))

        # generate variables
        date_items = []
        #date_item_template = { 'date': "",
        #                       'entries': [] }

        last_date = ""
        for page in content_pages:
            date = page.date_obj.strftime("%Y-%m-%d")
            if date != last_date:
                date_item = { 'date': date, 'entries': [ page ] }
                date_items.append(date_item)
            else:
                date_items[-1]['entries'].append(page)
            last_date = date

        self.variables['listing_by_date'] = True
        self.variables['date_items'] = date_items
