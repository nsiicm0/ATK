import os
from ATK.lib import Base
from typing import List, Dict
from google.cloud import texttospeech
import GoogleApiSupport.drive as drive
import GoogleApiSupport.slides as slides
from ATK.lib.Enums import SlideType, StepName


class GoogleApi(Base.Base):

    def __init__(self) -> None:
        self.slides_template_id = os.environ.get('SLIDES_TWEET_TEMPLATE')
        self.slides_trendy_folder_id = os.environ.get('SLIDES_TRENDY_FOLDER_ID')
        self.slides_upload_folder_id = os.environ.get('SLIDES_TWEETS_UPLOAD_FOLDER_ID')
        self.output_file = None

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def get_slides(self, **kwargs) -> None:
        tweets = list(filter(lambda x: x['step'] == f'{StepName.RENDER_TWEETS.value}_render_tweets' , kwargs['dependent_results']))[0]['results']
        name = f"{kwargs['title']} - {kwargs['UID']} "
        title = f"{kwargs['title']}"

        self.log_as.info(f'Creating new slides with name {title}')
        self.output_file = drive.copy_file(self.slides_template_id, name)
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
        slides.batch_text_replace({
            'TITLE': title
        }, self.output_file, [TITLE_SLIDE_ID])
        twitter_users = []
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
                self.log_as.info(f'Upload tweet')
                upload_response = drive.upload_image_to_drive(image_name=os.path.basename(tweet.render_path),
                                                              image_file_path=tweet.render_path,
                                                              folder_destination_id=self.slides_upload_folder_id)

                self.log_as.info(f'Adding tweet slide')
                response = slides.duplicate_object(self.output_file, SLIDE_HANDLES[SlideType.CONTENT.value]['objectId'])
                TWEET_SLIDE_ID = response['replies'][0]['duplicateObject']['objectId']  # this is already the objectId
                #we have to build a custom request in order to replace the image on just the current slide
                requests = [
                    {
                        "replaceAllShapesWithImage": {
                            "imageUrl": upload_response['image_url'],
                            "imageReplaceMethod": "CENTER_INSIDE",
                            "containsText": {
                                "text": "{{TWEET}}",
                            },
                            "pageObjectIds": [TWEET_SLIDE_ID]
                        }
                    }]
                slides.execute_batch_update(requests, self.output_file)
                twitter_users.append(f'@{tweet.handle}')

            # Move content template slide behind subtitle template slide
            self.log_as.info(f'Rearrange content template slide')
            slides.reindex_slides(presentation_id=self.output_file, slide_ids=[SLIDE_HANDLES[SlideType.CONTENT.value]['objectId']], new_index=3) # 3 should be the index right behind subtitle template

        self.log_as.info(f'Adding end slide')
        response = slides.duplicate_object(self.output_file, SLIDE_HANDLES[SlideType.END.value]['objectId'])
        END_SLIDE_ID = response['replies'][0]['duplicateObject']['objectId']
        credits = f'Credits to Twitter users: {", ".join(list(set(twitter_users[::-1])))}'
        slides.batch_text_replace({
            'CREDITS': credits
        }, self.output_file, [END_SLIDE_ID])

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

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def convert_tts(self, **kwargs) -> Dict:
        uid = kwargs['UID']
        dest_path = os.path.join('.', kwargs['SND_DIR'], uid)
        story = list(filter(lambda x: x['step'] == f'{StepName.DEVELOP_STORY.value}_develop', kwargs['dependent_results']))[0]['results']
        slide_images = list(filter(lambda x: x['step'] == f'{StepName.CONVERT_SLIDES.value}_convert_pdf_to_imgs', kwargs['dependent_results']))[0]['results']

        # prepare target dir
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()
        audio_info = dict()
        for slide, path in slide_images.items():
            slide_content = story.tell_slide(slide)
            audio_files = []
            for i, content in enumerate(slide_content):
                # Set the text input to be synthesized
                synthesis_input = texttospeech.SynthesisInput(text=content.view())
                # Build the voice request
                voice = texttospeech.VoiceSelectionParams(
                    language_code='en-US',
                    name="en-US-Wavenet-D",
                    ssml_gender=texttospeech.SsmlVoiceGender.MALE)
                # Select the type of audio file you want returned
                audio_config = texttospeech.AudioConfig(
                    speaking_rate=0.9,
                    audio_encoding=texttospeech.AudioEncoding.MP3)
                # Perform the text-to-speech request on the text input with the selected
                # voice parameters and audio file type
                response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
                # The response's audio_content is binary.
                target_name = os.path.join(dest_path, f'out_{str(slide).zfill(3)}_{str(i)}.mp3')
                with open(target_name, 'wb') as out:
                    # Write the response to the output file.
                    out.write(response.audio_content)
                    self.log_as.info(f'Audio content written to file: {target_name}')
                audio_files.append(target_name)
            audio_info[slide] = audio_files
        return audio_info
