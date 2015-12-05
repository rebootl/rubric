'''rubric page object'''

from Pages.ContentFilePage import ContentFilePage

class RubricPage(ContentFilePage):
    '''Main page of a rubric, e.g. Articles.'''

    def __init__(self, content_file, rubric):
        self.content_file = content_file
        self.rubric = rubric
        super().__init__( self.content_file,
                          out_subdir = self.rubric.name )

        self.type = "rubricpage"
        self.rubric.rubric_page = self

        self.variables['header_title'] = self.rubric.name
