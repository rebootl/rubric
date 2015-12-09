'''menu objects'''

import os

class RubricList:

    def __init__(self, site):
        self.site = site
        self.create_list()

    def create_list(self):
        ul = '<ul id="rubric-list">\n'

        li = '<li><a href="{}">{}</a></li>\n'

        span = '<span class="{}">{}</span>'

        # sort
        rubrics = self.site.rubrics.copy()

        rubrics.sort(key=lambda k: k.name)

        for rubric in rubrics:
            link_href = os.path.join('/', rubric.name)

            # entry count
            entry_cnt = len(rubric.pages)
            if entry_cnt > 1:
                entry_count_text = "{} entries".format(str(entry_cnt))
            else:
                entry_count_text = "1 entry"
            span_format = span.format('entry-count', entry_count_text)
            link_text = rubric.name + span_format
            ul = ul + li.format(link_href, link_text)

        self.menu = ul + '</ul>\n'
