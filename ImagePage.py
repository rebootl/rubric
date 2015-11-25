'''imagepage Page object'''
#
# using PIL (python-pillow) for image manipulation

import os
from PIL import Image, ImageOps

from ContentPage import ContentPage
from common import copy_file

class ImagePage(ContentPage):

    def __init__(self, content_file, rubric):
        super().__init__(content_file, rubric)

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
        image_body = '<img alt="{}" title="{}" src="{}" />'.format( img_alt,
                                                                    img_title,
                                                                    img_src )
        #self.body_md = image_body + self.body_md
        self.variables['imagepage-body'] = image_body

    def copy_image(self):
        copy_file(self.in_path_abs, self.out_dir_abs)

    def make_thumb(self):
        filename = os.path.basename(self.in_path_abs)
        out_filename = os.path.splitext(filename)[0] + "_thumb.png"
        self.out_filepath_abs = os.path.join( self.out_dir_abs,
                                              out_filename )

        image = Image.open(self.in_path_abs)

        thumb = ImageOps.fit(image, (256, 256), Image.ANTIALIAS)

        thumb.save(self.out_filepath_abs, "PNG")
