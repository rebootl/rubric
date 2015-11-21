'''menu objects'''

import os

class RubricList:

    def __init__(self, site):
        self.site = site
        self.create_list()

    def create_list(self):
        ul = '<ul id="rubric-list">\n'

        li = '<li><a href="{}">{}</a></li>\n'

        for rubric in self.site.rubrics:
            link_href = os.path.join('/', rubric.name)
            link_text = rubric.name
            ul = ul + li.format(link_href, link_text)

        self.menu = ul + '</ul>\n'
