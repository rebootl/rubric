'''file objects'''

import os
import json

class File:

    def __init__(self, subpath, name):
        self.subpath = subpath
        self.site = self.subpath.site
        self.name = name

        self.filepath_abs = os.path.join( subpath.site.config.CONTENT_DIR,
                                          subpath.subpath,
                                          name )
        print("File: ", self.filepath_abs)

class ContentFile(File):

    def __init__(self, subpath, name):
        super().__init__(subpath, name)

        self.meta, self.body_md = self.read_content_file()

        # set some more sane defaults
        if 'files' not in self.meta.keys():
            self.files = []
        else:
            self.files = self.meta['files']

        if 'type' not in self.meta.keys():
            self.type = 'norubric'
        else:
            self.type = self.meta['type']

        #print(self.meta)
        print("META: ")
        for key, val in self.meta.items():
            print(" ", key, ":", val)
        if 'rubric' not in self.meta.keys():
            if self.type == 'home':
                pass
            elif self.type == 'norubric':
                pass
            else:
                quit( "Error: {} type needs a rubric in header: {}".format(
                    self.type,
                    self.filepath_abs
                ) )
        else:
            self.rubric_name = self.meta['rubric']

    def read_content_file(self):
        with open(self.filepath_abs, 'r') as f:
            content = f.read()

        meta_json, body_md = content.split('%%%', 1)

        meta = json.loads(meta_json)

        # set sane defaults
        for key in self.site.config.DEFAULT_META_DICT:
            if key not in meta:
                meta[key] = self.site.config.DEFAULT_META_DICT[key]

        return meta, body_md
