from my_Gift_app.Models.Wallet.wallet import Wallet


def getWallet_by_Id(Id):
    try:
        wallet = Wallet.objects.select_related("userId").get(isDeleted=False,pk=Id)
        return wallet
    except:
        return None

def getAllWallet():
    try:
        list = Wallet.objects.select_related("userId").filter(isDeleted=False ).order_by("-Id")
        return list
    except Exception as ex:
        return None

def getWallet_by_UserId(userId):
    try:
        wallet=Wallet.objects.select_related("userId").get(isDeleted=False,userId=userId)
        return wallet
    except Exception as ex:
        return None