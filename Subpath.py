'''subpath object'''

import os

from File import ContentFile

class Subpath:

    def __init__(self, content, subpath=""):
        print("SUBPATH", subpath)
        self.content = content
        self.content.subpaths.append(self)
        self.site = content.site
        self.subpath = subpath

        self.path_abs = os.path.join(self.site.config.CONTENT_DIR, subpath)

        self.content_files = []
        self.subdirs = []

        self.load_content()

    def load_content(self):

        # get dir content
        dir_content = os.listdir(self.path_abs)

        subdirs = []
        # get content files
        for filename in dir_content:
            if filename.endswith(self.site.config.PAGE_EXT):
                file = ContentFile(self, filename)
                self.content_files.append(file)

            elif os.path.isdir( os.path.join( self.path_abs, filename) ):
                subdirs.append(filename)

        # recurse
        for subdir in subdirs:
            subpath_inst = Subpath(self.content, os.path.join(self.subpath, subdir))
            self.subdirs.append(subpath_inst)
