'''imagepage Page object'''
#
# using PIL (python-pillow) for image manipulation

import os
from PIL import Image, ImageOps

from Pages.ContentPage import ContentPage
from common import copy_file
import tags

class ImagePage(ContentPage):

    def __init__(self, content_file):
        super().__init__(content_file)
        self.type = 'imagepage'

        if not self.content_file.meta['image']:
            print("Warning: imagepage has no image set:", self.content_file.filepath_abs)
            pass
        self.imagefile = self.content_file.meta['image']

        self.img_in_path_abs = os.path.join( self.site.config.CONTENT_DIR,
                                             self.content_file.subpath.subpath,
                                             self.imagefile )
        self.make_thumb()

    def process(self):
        # sorting and page navigation (prev / index / next)
        self.set_next_page()
        self.set_prev_page()
        self.set_page_nav()

        self.add_image_body()

        # add menu
        #self.variables['rubric_list'] = self.site.rubric_list.menu

        self.render()
        self.write_out()

        # copy files
        self.copy_image()
        self.copy_files()

    def add_image_body(self):
        '''adding image body'''
        title = self.content_file.meta['title']
        img_alt = title
        img_title = title
        img_src = self.imagefile
        image_body = tags.IMG.format( "imagepage",
                                      img_alt,
                                      img_title,
                                      img_src )
        self.variables['body'] = image_body

    def copy_image(self):
        copy_file(self.img_in_path_abs, self.out_dir_abs)

    def make_thumb(self):
        in_filename = os.path.basename(self.img_in_path_abs)
        out_filename = os.path.splitext(in_filename)[0] + "_thumb.png"

        self.thumb_src = os.path.join('/', self.out_subdir, out_filename)
        self.out_thumbpath_abs = os.path.join( self.out_dir_abs,
                                          out_filename )

        # leave if already there
        if os.path.isfile(self.out_thumbpath_abs):
            return

        if not os.path.isdir(self.out_dir_abs):
            os.makedirs(self.out_dir_abs)

        image = Image.open(self.img_in_path_abs)

        thumb = ImageOps.fit(image, (256, 256), Image.ANTIALIAS)

        thumb.save(self.out_thumbpath_abs, "PNG")
