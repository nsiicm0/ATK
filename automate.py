import os
import random
import string
from ATK.Pipeline import *
from ATK.File.Api import File_Api
from ATK.Google.Api import Google_Api
from ATK.Twitter.Api import Twitter_Api
from ATK.Controller import ATK_Controller

def get_random_alphaNumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

if __name__ == '__main__':
    atk = ATK_Controller()

    pl = ATK_Pipeline()
    UID = get_random_alphaNumeric_string()
    config = dict({
        'title': f'Test Run #1{UID}',
        'n': 5,
        'UID': f'{UID}',
        'PDF_DIR': os.path.join('out','pdf'),
        'IMG_DIR': os.path.join('out','img')
    })
    s1 = ATK_Step(name='Get Tweets', obj=Twitter_Api(), calls=['get_tweets'], args=[config], prereqs=[])
    s2 = ATK_Step(name='Get Slides', obj=Google_Api(), calls=['get_slides','export_slides'], args=[config]*2, prereqs=['Get Tweets'])
    s3 = ATK_Step(name='Convert Slides', obj=File_Api(), calls=['convert_pdf_to_imgs'], args=[config], prereqs=['Get Slides'])

    pl.add_multiple_steps([s1,s2,s3])
    pl.run()
