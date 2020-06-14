import os
import random
import string
from datetime import date

from ATK.Pipeline import Pipeline
from ATK.File.Api import FileApi
from ATK.Google.Api import GoogleApi
from ATK.Step import Step
from ATK.StoryDeveloper import StoryDeveloper
from ATK.Twitter.Api import TwitterApi
from ATK.lib.Enums import StepName


def get_random_alphanumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

if __name__ == '__main__':
    UID = get_random_alphanumeric_string()
    today = date.today()
    date_string = today.strftime("%b %d, %Y")
    config = dict({
        'title': f'Trending Tweets for {date_string}',
        'country': 23424977,  # US tweets for now
        'n_topics': 10,
        'n_tweets_per_topic': 5,
        'UID': f'{UID}',
        'PDF_DIR': os.path.join('out', 'pdf'),
        'IMG_DIR': os.path.join('out', 'img'),
        'RDR_DIR': os.path.join('out', 'rdr'),
        'SND_DIR': os.path.join('out', 'snd'),
        'MOV_DIR': os.path.join('out', 'mov'),
        'BKP_DIR': os.path.join('out', 'bkp'),
    })
    pl = Pipeline(config=config)

    s1 = Step(name=StepName.GET_TWEETS, obj=TwitterApi(), calls=['get_tweets'], args=[dict({})], prereqs=[])
    s2 = Step(name=StepName.RENDER_TWEETS, obj=FileApi(), calls=['render_tweets'], args=[dict({})], prereqs=[StepName.GET_TWEETS])
    s3 = Step(name=StepName.DEVELOP_STORY, obj=StoryDeveloper(), calls=['develop'], args=[dict({})], prereqs=[StepName.RENDER_TWEETS])
    s4 = Step(name=StepName.GET_SLIDES, obj=GoogleApi(), calls=['get_slides', 'export_slides'], args=[dict({})] * 2, prereqs=[StepName.RENDER_TWEETS])
    s5 = Step(name=StepName.CONVERT_SLIDES, obj=FileApi(), calls=['convert_pdf_to_imgs'], args=[dict({})], prereqs=[StepName.GET_TWEETS,StepName.DEVELOP_STORY])
    s6 = Step(name=StepName.GET_TTS, obj=GoogleApi(), calls=['convert_tts'], args=[dict({})] * 1, prereqs=[StepName.CONVERT_SLIDES, StepName.DEVELOP_STORY])
    s7 = Step(name=StepName.STITCH_MOVIE, obj=FileApi(), calls=['convert_imgs_to_movie'], args=[dict({})] * 1, prereqs=[StepName.DEVELOP_STORY, StepName.CONVERT_SLIDES, StepName.GET_TTS])

    pl.add_multiple_steps([s1,s2,s3,s4,s5,s6,s7])
    pl.run()
