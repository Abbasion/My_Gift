from my_Gift_app.Models.SendReceiveCards.sendReceiveCards import SendReceiveCards
from my_Gift_app.Models.Users.users import User


def getAllSendCard():
    try:
        list = SendReceiveCards.objects.select_related("senderId","card").filter(isDeleted=False ).order_by("-Id")
        return list
    except Exception as ex:
        return None



def getReceiveCard_by_Id(Id):
    try:
        card=SendReceiveCards.objects.select_related("senderId","card").get(isDeleted=False,isClaimed=False,pk=Id)
        return card
    except:
        return None


def getReceiveCard_by_Phonenumber(receiverPhone):
    try:
        card=SendReceiveCards.objects.select_related("senderId","card").filter(isDeleted=False,receiverPhone=receiverPhone).order_by("-Id")
        return card
    except:
        return None

def getReceive_by_Phonenumber(PhoneNumber):
    try:
        user=User.objects.get(isDeleted=False,PhoneNumber=PhoneNumber)

        return user
    except:
        return None

def getSendCard_by_UserId(senderId):
    try:
        card=SendReceiveCards.objects.select_related("senderId","card").filter(isDeleted=False,senderId=senderId).order_by("-Id")
        return card
    except:
        return None


def Clamied_Card_by_UserId(senderId):
    try:
        card=SendReceiveCards.objects.select_related("senderId","card").filter(isDeleted=False,isClaimed=True,senderId=senderId).order_by("-Id")
        return card
    except:
        return None

def getAllClamiedSendCard():
    try:
        list = SendReceiveCards.objects.select_related("senderId","card").filter(isDeleted=False,isClaimed=True ).order_by("-Id")
        return list
    except Exception as ex:
        return None