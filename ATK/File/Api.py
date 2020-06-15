import os
import tempfile

from ATK.StoryElement import StoryElement
from ATK.Twitter.Api import Tweet
from ATK.lib import Base
from typing import List, Dict
from pdf2image import convert_from_path
import moviepy.editor as mpy
from selenium import webdriver
import time
from ATK.lib.Enums import SlideType, StepName


class FileApi(Base.Base):

    def __init__(self) -> None:
        pass

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def render_tweets(self, **kwargs) -> List[Dict]:
        uid = kwargs['UID']
        dest_path = os.path.join('.', kwargs['RDR_DIR'], uid)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)

        tweets = list(filter(lambda x: x['step'] == f'{StepName.GET_TWEETS.value}_get_tweets', kwargs['dependent_results']))[0]['results']
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        self.log_as.info(f'Generating tweets from oembed')
        for obj in tweets:
            content = obj['content']
            for tweet in content:
                oembed = tweet.oembed
                driver.execute_script("""
                    document.location = 'about:blank';
                    document.open();
                    document.write(arguments[0]);
                    document.close();
                    """, oembed['html'])
                time.sleep(2)
                #driver.execute_script("document.body.style.zoom='200%'") # this will make images in higher resolution
                image = driver.find_elements_by_class_name('twitter-tweet-rendered')[0].screenshot_as_png
                file_path = os.path.join(dest_path, f'{tweet.id}.png')
                with open(file_path, 'wb') as fp:
                    fp.write(image)
                tweet.render_path = file_path
        driver.quit()
        return tweets

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def convert_pdf_to_imgs(self, **kwargs) -> Dict:
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
        uid = kwargs['UID']
        slide_images =list(filter(lambda x: x['step'] == f'{StepName.CONVERT_SLIDES.value}_convert_pdf_to_imgs', kwargs['dependent_results']))[0]['results']
        slide_sounds = list(filter(lambda x: x['step'] == f'{StepName.GET_TTS.value}_convert_tts', kwargs['dependent_results']))[0]['results']
        sld_clips = []
        t = 0
        for (imgkey, imgval), (sndkey, sndvals) in zip(slide_images.items(), slide_sounds.items()):
            audio_clips = []
            t_a = 0
            for snd in sndvals:
                _audio = mpy.AudioFileClip(snd)
                audio_clips.append(_audio.set_start(t_a))
                # account for current audio clip length
                t_a = _audio.duration

            sld_audio = mpy.concatenate_audioclips(audio_clips)
            sld = (mpy.ImageClip(imgval)
                 .set_duration(sld_audio.duration)  # using the fx library to effortlessly transform the video clip # .on_color(size=DIM, color=dark_grey)
                 .set_fps(5) # if we want to use transition we would need to increase fps to > 24
                 .set_audio(sld_audio))
            sld_clips.append(sld.set_start(t))
            # account for current compound clip length
            t += sld.duration
        video = mpy.CompositeVideoClip(sld_clips)

        # prepare target dir
        dest_path = os.path.join('.', kwargs['MOV_DIR'])
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)

        video_path = os.path.join(dest_path, f'{uid}.mp4')
        video.write_videofile(video_path, threads=4, logger=None)
