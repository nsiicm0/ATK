import os
import tempfile
from ATK.lib import Base
from typing import List, Dict
from pdf2image import convert_from_path

class FileApi(Base.Base):

    def __init__(self) -> None:
        pass

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def convert_pdf_to_imgs(self, **kwargs) -> List[str]:
        uid = kwargs['UID']
        source_path = os.path.join('.', kwargs['PDF_DIR'], f'{uid}.pdf')
        dest_path = os.path.join('.', kwargs['IMG_DIR'], uid)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        slide_info = dict()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(source_path, dpi=500, output_folder=path)
            for i, page in enumerate(images_from_path):
                image_name = os.path.join(dest_path, f'out_{str(i).zfill(3)}.png')
                page.save(image_name, 'PNG')
                slide_info[i] = image_name
        return slide_info

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def convert_imgs_to_movie(self, **kwargs) -> None:
        pass