import os
import random
import string

from ATK.Pipeline import Pipeline
from ATK.File.Api import FileApi
from ATK.Google.Api import GoogleApi
from ATK.Step import Step
from ATK.StoryDeveloper import StoryDeveloper
from ATK.Twitter.Api import TwitterApi
from ATK.Controller import Controller
from ATK.lib.Enums import StepName


def get_random_alphanumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

if __name__ == '__main__':
    atk = Controller()

    pl = Pipeline()
    UID = get_random_alphanumeric_string()
    config = dict({
        'title': f'Test Run #1{UID}',
        'n': 5,
        'query': '#Test_query',
        'UID': f'{UID}',
        'PDF_DIR': os.path.join('out','pdf'),
        'IMG_DIR': os.path.join('out','img')
    })
    s1 = Step(name=StepName.GET_TWEETS, obj=TwitterApi(), calls=['get_tweets'], args=[config], prereqs=[])
    s2 = Step(name=StepName.DEVELOP_STORY, obj=StoryDeveloper(), calls=['develop'], args=[config], prereqs=[StepName.GET_TWEETS])
    s3 = Step(name=StepName.GET_SLIDES, obj=GoogleApi(), calls=['get_slides', 'export_slides'], args=[config] * 2, prereqs=[StepName.GET_TWEETS])
    s4 = Step(name=StepName.CONVERT_SLIDES, obj=FileApi(), calls=['convert_pdf_to_imgs'], args=[config], prereqs=[StepName.GET_TWEETS])

    pl.add_multiple_steps([s1, s2])
    pl.run()
