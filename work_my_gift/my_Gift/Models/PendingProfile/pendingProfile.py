import base64
import datetime
import json
import math

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift import settings
from my_Gift.Helper.PendingProfileHelper.pendingProfileHelper import getPendingProfile_by_UserId, getallPendingprfiles, \
    getAllPartners, PendingProfiles_byId
from my_Gift.Helper.Users.Users import getUser_by_Id, getAdmin
from my_Gift.settings import IMG_URL
from my_Gift_app.Models.Nitifications.notifications import Notifications
from my_Gift_app.Models.PendingProfile.pendingProfile import PendingProfile
from my_Gift_app.Models.Users.userSerializer import UserSerializer


class PendingProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            dic = request.data
            user = request.user  # getUser_by_Id(dic['userId'])
            pending_profile = getPendingProfile_by_UserId(user)


            if pending_profile is None:

                profile = PendingProfile(
                    userId=user
                )

                # Email=user.Email,
                if ("UserName" in dic.keys()):
                    profile.UserName = dic['UserName']
                if ("Country" in dic.keys()):
                    profile.Country = dic['Country']

                if ("address" in dic.keys()):
                    profile.address = dic['address']
                if ("PhoneNumber" in dic.keys()):
                    profile.PhoneNumber = dic['PhoneNumber']
                if ("isDeleted" in dic.keys()):
                    profile.isDeleted = dic['isDeleted']
                profile.Email = user.Email
                profile.status = 0

                if ("profilePic" in dic.keys()):
                    if (isinstance(dic['profilePic'], dict)):
                        if ("fileName" in dic["profilePic"].keys()):
                            url = dic['profilePic']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            print(url)
                            name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + str(
                                dic['profilePic']['fileName'])
                            # print(name)
                            filename = str(settings.BASE_DIR) + r"\myGift/uploads/" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()
                                profile.profilePic = name

                profile.save()
                Admins = getAdmin()
                for admin in Admins:
                    notification = Notifications(
                        notification_by=user,
                        notification_to=admin,
                        description=profile.UserName + " has request to update his profile "
                    )
                    notification.save()

                    notification = Notifications(
                        notification_by=admin,
                        notification_to=user,
                        description=profile.UserName + " has request to update his profile "
                    )
                    notification.save()
                data = model_to_dict(profile)

                data['userId'] = (UserSerializer(profile.userId)).data
                if (profile.userId.profilePic):
                    data['userId']['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(profile.userId.profilePic)
                if (profile.profilePic):
                    data['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(profile.profilePic)

                    # newData = model_to_dict(send)
                    # if (send.cardPic):
                    #     pp = str(IMG_URL) + "/myGift/uploads/" + str(name)
                    #     newData['cardPic'] = pp

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
            else:

                pending_profile.userId = user
                if ('status' in dic.keys()):
                    pending_profile.status = dic['status']
                else:
                    return Response(
                        {"data": "status is required", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST
                    )


                if ("UserName" in dic.keys()):
                    pending_profile.UserName = dic['UserName']
                if ("Country" in dic.keys()):
                    pending_profile.Country = dic['Country']
                if ("address" in dic.keys()):
                    pending_profile.address = dic['address']

                # pending_profile.PhoneNumber = dic['PhoneNumber']
                if ("status" in dic.keys()):
                    pending_profile.status = dic['status']
                if ("isDeleted" in dic.keys()):
                    pending_profile.isDeleted = dic['isDeleted']
                if ("profilePic" in dic.keys()):
                    if (isinstance(dic['profilePic'], dict)):
                        if ("fileName" in dic["profilePic"].keys()):
                            url = dic['profilePic']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + dic['profilePic'][
                                'fileName']
                            filename = str(settings.BASE_DIR) + r"\myGift/uploads\\" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()
                                pending_profile.profilePic = name

                # pending_profile.profilePic = dic['profilePic']

                # card = PendingProfile.objects.get(pk=dic['Id'])

                pending_profile.save()
                Admins = getAdmin()
                if (dic['status'] == 1):
                    user.UserName = pending_profile.UserName
                    user.address = pending_profile.address
                    user.Country = pending_profile.Country
                    user.profilePic = pending_profile.profilePic
                    user.save()
                    notification = Notifications(
                        notification_by=Admins[0],
                        notification_to=user,
                        description="Dear " + user.UserName + " your profile has been updated "
                    )
                    notification.save()

                for admin in Admins:
                    notification = Notifications(
                        notification_by=user,
                        notification_to=admin,
                        description=user.UserName + " has request to Re-update his profile "
                    )
                    notification.save()

                data = model_to_dict(pending_profile)
                del data['Email']
                # print(data)

                data['userId'] = (UserSerializer(pending_profile.userId)).data

                if (pending_profile.userId.profilePic):
                    data['userId']['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(
                        pending_profile.userId.profilePic)
                if (pending_profile.profilePic):
                    data['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(pending_profile.profilePic)
                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            pending_profile = getallPendingprfiles()
            for profile in pending_profile:
                profileData = model_to_dict(profile)
                profileData['userId'] = UserSerializer(profile.userId).data
                if (profile.userId.profilePic):
                    profileData['userId']['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(
                        profile.userId.profilePic)
                if (profile.profilePic):
                    profileData['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(profile.profilePic)
                data.append(profileData)
            return Response({"data": data, "status": status.HTTP_200_OK})

        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})


class GetAllPartnerAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            users = getAllPartners()
            data = []

            for user in users:
                serializer = self.serializer_class(user)
                newData = serializer.data
                if (user.profilePic):
                    newData['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(user.profilePic)

                # if (user.profilePic and user.isSocial == False):
                #     pp = str(IMG_URL) + "/myGift/uploads/" + str(user.profilePic)
                #     newData['profilePic'] = pp
                data.append(newData)

            # print(serializer.data)
            return Response({"data": data, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PendingProfileBYUserIdUpdateToUserAPIView(RetrieveUpdateAPIView):

    def post(self,request):
        try:

            newData={}
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            if ('userId' in dic.keys()):
                userId = dic['userId']
            else:
                return Response(
                    {"data": "userId is required", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )

            profile = PendingProfiles_byId(dic['userId'])
            print(profile.status,profile.UserName)


            if (profile is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            elif 'status' not in dic.keys():
                return Response(
                    {"data": "status is required", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )


            else:
                data = model_to_dict(profile)
                data['userId'] = UserSerializer(profile.userId).data
                if (dic['status']==1):
                    user = getUser_by_Id(userId)
                    profile.status = dic['status']
                    profile.save()

                    user.isDeleted = profile.isDeleted

                    user.UserName = profile.UserName
                    user.Country = profile.Country
                    user.address = profile.address
                    user.PhoneNumber = profile.PhoneNumber
                    user.p_profilePic = profile.profilePic
                    user.save()
                    Admins = getAdmin()
                    notification = Notifications(
                        notification_to=user.Id,
                        notification_by=Admins[0],
                        description=user.UserName+" your profile has successfully updated"
                    )
                    notification.save()
                    print(notification)
                    serializer = UserSerializer(user)
                    newData = serializer.data
                    if (user.profilePic):
                        newData['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(user.profilePic)
                    # if (user.profilePic and user.isSocial == False):
                    #     pp = str(IMG_URL) + "/myGift/uploads/" + str(user.profilePic)
                    #     newData['profilePic'] = pp




            return Response({"data": newData, "status": 201}, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)