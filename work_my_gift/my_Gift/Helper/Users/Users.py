

from my_Gift_app.Models.Users.users import User


def getUser_by_Id(Id):
    try:
        users = User.objects.get(pk=Id,isDeleted=False)
        return users
    except Exception as ex:
        return None
def getUser_by_Mail(Email):
    try:
        users = User.objects.get(Email=Email,isDeleted=False)
        return users
    except:
        return None
def getUser_by_Phone(ph):
    try:
        users = User.objects.get(PhoneNumber=ph,isDeleted=False)
        return users
    except Exception as ex:
        return None

def getUser_by_Ph(ph):
    try:
        users = User.objects.get(PhoneNumber=ph,isDeleted=False)
        return users
    except:
        return None

def getUsers():
    try:
        users = User.objects.filter(isDeleted=False).order_by("-Id")
        return users
    except :
        return []

def getAdmin():
    try:
        users = User.objects.filter(isDeleted=False,RoleType=0).order_by("-Id")
        return users
    except :
        return []