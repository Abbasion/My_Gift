from my_Gift_app.Models.PendingProfile.pendingProfile import PendingProfile
from my_Gift_app.Models.Users.users import User


def getPendingProfile_by_UserId(userId):
    try:
        users = PendingProfile.objects.get(userId=userId, isDeleted=False)
        return users
    except Exception as ex:

        return None


def getallPendingprfiles():
    try:
        list = PendingProfile.objects.select_related("userId").filter(isDeleted=False).order_by("-Id")
        return list
    except:
        return None


def getPendingProfile_by_UserIdandStatus(userId):
    try:
        Profile = PendingProfile.objects.select_related("userId").filter(isDeleted=False, userId=userId,
                                                                         status=0).order_by("-Id")

        return Profile
    except:
        return None


def getAllPartners():
    try:
        users = User.objects.filter(isDeleted=False, RoleType=1).order_by("-Id")
        return users
    except:
        return []


def PendingProfiles_byId(userId):
    try:
        profile = PendingProfile.objects.get(userId=userId, isDeleted=False)
        return profile
    except:
        return None