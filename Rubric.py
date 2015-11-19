'''rubric object'''

class Rubric:

    def __init__(self, site, name):
        self.site = site
        self.site.rubrics.append(self)
        self.name = name

        self.pages = []
