

from my_Gift.settings import IMG_URL


def img_url(name):
            return  str(IMG_URL)+r"\myGift/uploads\\"+name


def img_url_profile(name):
    return str(IMG_URL) + r"\myGift/uploads\\" + name