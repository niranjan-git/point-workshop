from django.conf import settings
import random
from six import u

def generateCustomCaptcha():
    chars, ret = u("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"), u("")

    captcha = ""
    n = settings.CAPTCHA_LENGTH
    while (n):
        ret += chars[random.randint(1, 1000) % 62]
        n -= 1
    print("Captcha: ",ret)
    return ret, ret

# generateCustomCaptcha()


