import os
from ATK.lib import Base
from typing import List, Dict
import GoogleApiSupport.drive as drive
import GoogleApiSupport.slides as slides

class Google_Api(Base.Base):

    def __init__(self) -> None:
        self.slides_template_id = os.environ.get('SLIDES_TWEET_TEMPLATE')
        self.slides_trendy_folder_id = os.environ.get('SLIDES_TRENDY_FOLDER_ID')
        self.output_file = None
        #TEMPLATE = slides.get_presentation_info(self.slides_template_id)['slides'][0]['pageElements'][0]

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def get_slides(self, **kwargs) -> None:
        tweets = kwargs['previous_results']
        title = kwargs['title']
        self.log_as.info(f'Creating new slides with name {title}')
        self.output_file = drive.copy_file(self.slides_template_id, title)
        self.log_as.info(f'Move to appropriate location')
        drive.move_file(self.output_file, self.slides_trendy_folder_id)
        self.log_as.info(f'Getting handle of template slides')
        slide_elements = iter(slides.get_presentation_slides(self.output_file))
        title_slide = next(slide_elements)
        trend_title_slide = next(slide_elements)
        tweet_slide = next(slide_elements)

        # add trend slide
        self.log_as.info(f'Adding trend slide')
        response = slides.duplicate_object(self.output_file, trend_title_slide['objectId'])
        TREND_SLIDE = response['replies'][0]['duplicateObject']['objectId']
        slides.batch_text_replace({
            'TREND': '#TEST'
        }, self.output_file, [TREND_SLIDE])

        for tweet in tweets:
            self.log_as.info(f'Adding tweet slide')
            response = slides.duplicate_object(self.output_file, tweet_slide['objectId'])
            TWEET_SLIDE = response['replies'][0]['duplicateObject']['objectId'] # this is already the objectId
            slides.batch_text_replace({
                'NAME': tweet.name,
                'USERNAME': tweet.handle,
                'TEXT': tweet.text,
                'DATE': tweet.date
            }, self.output_file, [TWEET_SLIDE])

        self.log_as.info(f'Removing template slides')
        slides.delete_object(self.output_file, trend_title_slide['objectId'])
        slides.delete_object(self.output_file, tweet_slide['objectId'])

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def export_slides(self, **kwargs) -> None:
        uid = kwargs['UID']
        dest_path = os.path.join('.',kwargs['PDF_DIR'])
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        dest_file = os.path.join(dest_path, f'{uid}.pdf')
        drive.download_file(self.output_file, destination_path=dest_file, mime_type='application/pdf')

