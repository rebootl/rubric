'''special page object'''

import os

from Pages.ContentFilePage import ContentFilePage

class SpecialPage(ContentFilePage):
    '''top level pages beside homepage, e.g. about, links etc..'''

    def __init__(self, content_file):
        self.content_file = content_file
        out_filename = os.path.splitext(content_file.name)[0] + '.html'
        # (evtl. change to "url encoded" later)

        super().__init__( self.content_file,
                          out_filename = out_filename )

        self.type = 'specialpage'

        #self.variables['header_title'] = self.variables['title']
        self.variables['article_title'] = True
