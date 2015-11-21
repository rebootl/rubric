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

class ContentFile(File):

    def __init__(self, subpath, name):
        super().__init__(subpath, name)

        self.meta, self.body_md = read_content_file(self.filepath_abs)

        if 'files' not in self.meta.keys():
            self.files = []
        else:
            self.files = self.meta['files']

        if 'type' not in self.meta.keys():
            self.type = None
        else:
            self.type = self.meta['type']


DEFAULT_META_DICT = { 'title': "Warning: No title set in content file.",
                      'author': "Warning: No author set in content file.",
                      'date': "Warning: No date set in content file."  }

def read_content_file(filepath_abs):

    with open(filepath_abs, 'r') as f:
         content = f.read()

    meta_json, body_md = content.split('%%%', 1)

    meta = json.loads(meta_json)

    # set sane defaults
    for key in DEFAULT_META_DICT:
        if key not in meta:
            meta[key] = DEFAULT_META_DICT[key]

    return meta, body_md
