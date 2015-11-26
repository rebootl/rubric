'''imagepage Page object'''
#
# using PIL (python-pillow) for image manipulation

import os
from PIL import Image, ImageOps

from ContentPage import ContentPage
from common import copy_file

IMG = '<img class="imagepage" alt="{}" title="{}" src="{}" />'

class ImagePage(ContentPage):

    def __init__(self, content_file, rubric):
        super().__init__(content_file, rubric)
        self.type = 'imagepage'

        self.imagefile = self.meta['image']

        self.in_path_abs = os.path.join( self.site.config.CONTENT_DIR,
                                         self.subpath.subpath,
                                         self.imagefile )

        self.out_dir_abs = os.path.join( self.site.config.PUBLISH_DIR,
                                         self.out_dir )

        self.preprocess()

        self.add_image_body()
        self.copy_image()
        self.make_thumb()

    def add_image_body(self):
        # --> add $image-body$ html
        # self.meta.image
        img_alt = self.title
        img_title = self.title
        img_src = self.imagefile
        image_body = IMG.format( img_alt,
                                 img_title,
                                 img_src )
        #self.body_md = image_body + self.body_md
        self.variables['imagepage-body'] = image_body

    def copy_image(self):
        copy_file(self.in_path_abs, self.out_dir_abs)

    def make_thumb(self):
        in_filename = os.path.basename(self.in_path_abs)
        out_filename = os.path.splitext(in_filename)[0] + "_thumb.png"

        self.thumb_src = os.path.join(self.out_dir, out_filename)
        self.out_thumbpath_abs = os.path.join( self.out_dir_abs,
                                          out_filename )

        # leave if already there
        if os.path.isfile(self.out_thumbpath_abs):
            return

        image = Image.open(self.in_path_abs)

        thumb = ImageOps.fit(image, (256, 256), Image.ANTIALIAS)

        thumb.save(self.out_thumbpath_abs, "PNG")
