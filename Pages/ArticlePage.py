'''article page object'''

from Pages.ContentPage import ContentPage

class ArticlePage(ContentPage):

    def __init__(self, content_file):
        super().__init__(content_file)

        self.type = 'article'
        self.variables['article_title'] = True
