import os
import tempfile
from ATK.lib import Base
from typing import List, Dict
from pdf2image import convert_from_path

class File_Api(Base.Base):

    def __init__(self) -> None:
        pass

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def convert_pdf_to_imgs(self, **kwargs) -> None:
        uid = kwargs['UID']
        source_path = os.path.join('.', kwargs['PDF_DIR'], f'{uid}.pdf')
        dest_path = os.path.join('.', kwargs['IMG_DIR'], uid)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)

        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(source_path, dpi=500, output_folder=path)
            for i, page in enumerate(images_from_path):
                page.save(os.path.join(dest_path, f'out_{str({i}).zfill(3)}.png'), 'PNG')