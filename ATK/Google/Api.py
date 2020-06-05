import os
from ATK.lib import Base
from typing import List, Dict
import GoogleApiSupport.drive as drive
import GoogleApiSupport.slides as slides

from ATK.lib.Enums import SlideType, StepName


class GoogleApi(Base.Base):

    def __init__(self) -> None:
        self.slides_template_id = os.environ.get('SLIDES_TWEET_TEMPLATE')
        self.slides_trendy_folder_id = os.environ.get('SLIDES_TRENDY_FOLDER_ID')
        self.output_file = None

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def get_slides(self, **kwargs) -> None:
        tweets = list(filter(lambda x: x['step'] == StepName.GET_TWEETS , kwargs['dependent_results']))[0]['results']
        title = kwargs['title']
        self.log_as.info(f'Creating new slides with name {title}')
        self.output_file = drive.copy_file(self.slides_template_id, title)
        self.log_as.info(f'Move to appropriate location')
        drive.move_file(self.output_file, self.slides_trendy_folder_id)
        self.log_as.info(f'Getting handle of template slides')
        slds = slides.get_presentation_slides(self.output_file)
        SLIDE_HANDLES = dict()
        for slide in slds:
            notes = slides.get_slide_notes(slide).strip()
            if notes in list(map(lambda x: x.value, SlideType)):
                SLIDE_HANDLES[notes] = slide

        self.log_as.info(f'Adding title slide')
        response = slides.duplicate_object(self.output_file, SLIDE_HANDLES[SlideType.TITLE.value]['objectId'])
        TITLE_SLIDE_ID = response['replies'][0]['duplicateObject']['objectId']

        for obj in tweets[::-1]:
            # add trend slide
            self.log_as.info(f'Adding trend slide')
            response = slides.duplicate_object(self.output_file, SLIDE_HANDLES[SlideType.SUBTITLE.value]['objectId'])
            TREND_SLIDE_ID = response['replies'][0]['duplicateObject']['objectId']
            slides.batch_text_replace({
                'TREND': obj['query']
            }, self.output_file, [TREND_SLIDE_ID])

            content = obj['content']
            for tweet in content[::-1]:
                self.log_as.info(f'Adding tweet slide')
                response = slides.duplicate_object(self.output_file, SLIDE_HANDLES[SlideType.CONTENT.value]['objectId'])
                TWEET_SLIDE_ID = response['replies'][0]['duplicateObject']['objectId']  # this is already the objectId
                slides.batch_text_replace({
                    'NAME': tweet.name,
                    'USERNAME': tweet.handle,
                    'TEXT': tweet.text,
                    'DATE': tweet.date
                }, self.output_file, [TWEET_SLIDE_ID])

            # Move content template slide behind subtitle template slide
            self.log_as.info(f'Rearrange content template slide')
            slides.reindex_slides(presentation_id=self.output_file, slide_ids=[SLIDE_HANDLES[SlideType.CONTENT.value]['objectId']], new_index=3) # 3 should be the index right behind subtitle template

        self.log_as.info(f'Adding end slide')
        response = slides.duplicate_object(self.output_file, SLIDE_HANDLES[SlideType.END.value]['objectId'])
        END_SLIDE_ID = response['replies'][0]['duplicateObject']['objectId']

        self.log_as.info(f'Removing template slides')
        for template_slide in SLIDE_HANDLES.values():
            slides.delete_object(self.output_file, template_slide['objectId'])


    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def export_slides(self, **kwargs) -> None:
        uid = kwargs['UID']
        dest_path = os.path.join('.',kwargs['PDF_DIR'])
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        dest_file = os.path.join(dest_path, f'{uid}.pdf')
        drive.download_file(self.output_file, destination_path=dest_file, mime_type='application/pdf')

