'''home page object'''

from Pages.ContentFilePage import ContentFilePage

class HomePage(ContentFilePage):
    '''The home page, /index.html.'''

    def __init__(self, content_file):
        self.content_file = content_file
        super().__init__(self.content_file)

        self.type = "homepage"
