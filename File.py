'''file objects'''

import os
import json

import config

class File:

    def __init__(self, name, subpath):
        self.name = name
        self.subpath = subpath

        self.filepath_abs = os.path.join(config.CONTENT_DIR, subpath, name)


class ContentFile(File):

    def __init__(self, name, subpath):
        super().__init__(name, subpath)

        self.meta, self.body_md = read_content_file(self.filepath_abs)


DEFAULT_META_DICT = { 'title': "Warning: No title set in content file.",
                      'author': "Warning: No author set in content file.",
                      'date': "Warning: No date set in content file.",
                      'type': "None",
                      'files': [] }

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
