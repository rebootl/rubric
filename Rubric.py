'''rubric object'''

class Rubric:

    def __init__(self, site, name):
        self.site = site
        self.site.rubrics.append(self)
        self.name = name

        self.pages = []
        #self.articles = []
        #self.images = []

    def sort(self):
        self.pages = sort_pages(self.pages)

        for page in self.pages:
            page.sort()



def sort_pages(pages):
    try:
        pages.sort(key=lambda k: k.title)
    except AttributeError:
        print("Warning: Bad title, can't properly sort...")
        pass
    try:
        pages.sort(key=lambda k: k.date_obj.timestamp())
    except AttributeError:
        print("Warning: Bad date, can't properly sort...")
        pass
    return pages
