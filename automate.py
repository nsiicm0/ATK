import os
import random
import string
from ATK.Pipeline import *
from ATK.File.Api import FileApi
from ATK.Google.Api import GoogleApi
from ATK.Step import Step
from ATK.Twitter.Api import TwitterApi
from ATK.Controller import Controller

def get_random_alphaNumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

if __name__ == '__main__':
    atk = Controller()

    pl = Pipeline()
    UID = get_random_alphaNumeric_string()
    config = dict({
        'title': f'Test Run #1{UID}',
        'n': 5,
        'query': '#Test_query',
        'UID': f'{UID}',
        'PDF_DIR': os.path.join('out','pdf'),
        'IMG_DIR': os.path.join('out','img')
    })
    s1 = Step(name='Get Tweets', obj=TwitterApi(), calls=['get_tweets'], args=[config], prereqs=[])
    s2 = Step(name='Get Slides', obj=GoogleApi(), calls=['get_slides', 'export_slides'], args=[config] * 2, prereqs=['Get Tweets'])
    s3 = Step(name='Convert Slides', obj=FileApi(), calls=['convert_pdf_to_imgs'], args=[config], prereqs=['Get Slides'])

    pl.add_multiple_steps([s1])
    pl.run()
