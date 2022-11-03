import datetime

from my_Gift.Helper.EncryptAndDecryptHelper.encryptAndDecryptHelper import encrypt
from my_Gift_app.Models.Cards.cards import Cards


def generateCartId(card,userId):
    timeStamp = datetime.datetime.now().timestamp()
    data = str(card.Id)+"_"+str(card.userId.Id)+"_"+str(timeStamp)+str(userId)

    return encrypt(data)


def getCard_by_Id(Id):
    try:
        card = Cards.objects.get(pk=Id,isDeleted=False)
        return card
    except:
        return None



def getallcards():
    try:
        list = Cards.objects.select_related("userId").filter(isDeleted=False).order_by("-Id")
        return list
    except:
        return None