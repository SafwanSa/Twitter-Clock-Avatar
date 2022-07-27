import base64
from io import BytesIO
from PIL import Image
import datetime 
import math
import os
import requests
import tweepy
import environ

class ImageGenerator:

    def __init__(self) -> None:
        pass
        
    def _get_rotated_img(self, original, angle) -> Image:
        rotated = original.rotate(-angle)
        rotated.name = f'{original.filename}_{angle}.png'
        return rotated

    def _get_current_angle(self) -> int:
        hours = 12
        angels = 360
        current_hour = datetime.datetime.now().hour % 12
        current_angle = int((current_hour/hours) * angels)
        return current_angle

    def _overlay_clock(self, img) -> int:
        clock = Image.open("docs/clock.png").convert("RGBA")
        x, y = img.size
        img.paste(clock, (0, 0, x, y), mask = clock)
        return img

    def generate(self, path):
        original = Image.open(path)
        angle = self._get_current_angle()
        rotated = self._get_rotated_img(original=original, angle=angle)
        result = self._overlay_clock(img=rotated)
        return result
    
    def im_2_b64(self, image):
        buff = BytesIO()
        image.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue())
        return img_str

    def im_2_bytes(self, image):
        buf = BytesIO()
        image.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        return byte_im

class TwitterManager:
    
    def __init__(self) -> None:
        env = environ.Env()
        env.read_env('.env')
        self.API_KEY = env('API_KEY')
        self.API_KEY_SECRET = env('API_KEY_SECRET')
        self.ACCESS_TOKEN = env('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = env('ACCESS_TOKEN_SECRET')
    
    def update_profile_pic(self, pic):
        auth = tweepy.OAuthHandler(self.API_KEY,self.API_KEY_SECRET,)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.verify_credentials()
        api.update_profile_image(filename='pic',file=pic)

def main():
    image_generator = ImageGenerator()
    img = image_generator.generate('docs/me.png').convert('RGB')
    tm = TwitterManager()
    tm.update_profile_pic(image_generator.im_2_bytes(img))
    
if __name__ == '__main__':
    # main()
    pass
    

def cronjob():
    """
    Main cron job.
    The main cronjob to be run continuously.
    """
    print("Cron job is running")
    print("Tick! The time is: %s" % datetime.datetime.now())