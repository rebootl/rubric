'''page objects'''

# a page consists of a content file,
# plus additional files like embedded images etc.
#
# content file
# ------------
#
# 1) meta information at the beginning using json format
#    e.g.:
#    {
#      "title":  "Welcome Home",
#      "author": "Cem",
#      "date":   "2015-11-16",
#      "type":   "home page",
#      "files":  []
#    }
#    %%%
#
#    delimited by "%%%"
#
# 2) page content in markdown and/or plugin syntax (optional)


class Page:

    def __init__(self, content_file):
        self.content_file = content_file

        self.title = content_file.meta['title']
        self.author = content_file.meta['author']
        self.date = content_file.meta['date']
        self.type = content_file.meta['type']
        self.files = content_file.meta['files']

class HomePage(Page):

    def __init__(self, content_file):
        super().__init__(content_file)

        self.out_path = ""
        self.out_filename = "index.html"

        self.template = "default.html5"
