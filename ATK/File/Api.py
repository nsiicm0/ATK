import os
import tempfile

from ATK.StoryElement import StoryElement
from ATK.Twitter.Api import Tweet
from ATK.lib import Base
from typing import List, Dict
from pdf2image import convert_from_path
import moviepy.editor as mpy

from ATK.lib.Enums import SlideType, StepName


class FileApi(Base.Base):

    def __init__(self) -> None:
        pass

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
        story = list(filter(lambda x: x['step'] == f'{StepName.DEVELOP_STORY.value}_develop', kwargs['dependent_results']))[0]['results']
        '''slide_images = dict({0: './out/img/NFVl62sA/out_000.png', 1: './out/img/NFVl62sA/out_001.png',
                             2: './out/img/NFVl62sA/out_002.png', 3: './out/img/NFVl62sA/out_003.png',
                             4: './out/img/NFVl62sA/out_004.png', 5: './out/img/NFVl62sA/out_005.png',
                             6: './out/img/NFVl62sA/out_006.png', 7: './out/img/NFVl62sA/out_007.png'})
        slide_sounds = dict({0: ['./out/snd/NFVl62sA/out_000_0.mp3'],
                            1: ['./out/snd/NFVl62sA/out_001_0.mp3'],
                            2: ['./out/snd/NFVl62sA/out_002_0.mp3'],
                            3: ['./out/snd/NFVl62sA/out_003_0.mp3'],
                            4: ['./out/snd/NFVl62sA/out_004_0.mp3'],
                            5: ['./out/snd/NFVl62sA/out_005_0.mp3'],
                            6: ['./out/snd/NFVl62sA/out_006_0.mp3'],
                            7: ['./out/snd/NFVl62sA/out_007_0.mp3']})
                            '''
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
        video.write_videofile(video_path, threads=4)
