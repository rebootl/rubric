'''contentpage Page object'''

import os
import re

from Page import Page

class ContentPage(Page):

    def __init__(self, content_file, rubric):
        super().__init__(content_file)
        self.rubric = rubric
        self.rubric.pages.append(self)

        self.out_filename = url_encode_filename(self.title) + '.html'
        if not self.date_obj:
            print("Warning: Erroneous date:", self.content_file.filepath_abs)
            date_str = "ERRONEOUS_DATE"
        else:
            date_str = self.date_obj.strftime("%Y-%m-%d")
        self.out_dir = os.path.join( self.rubric.name,
                                     date_str )

        self.header_title = self.rubric.name

        self.preprocess()

def url_encode_filename(string):
    # 1) convert spaces to dashes
    dashed = re.sub(r'[\ ]', '-', string)
    # 2) only accept [^a-zA-Z0-9-]
    #    replace everything else by %
    alnum_dashed = re.sub(r'[^a-zA-Z0-9-]', '-', dashed)
    # 3) lowercase
    return alnum_dashed.lower()
