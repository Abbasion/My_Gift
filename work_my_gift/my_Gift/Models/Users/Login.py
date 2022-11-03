import base64
import datetime
import json
import math
import os

from django.contrib.auth import authenticate, user_logged_in
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from my_Gift import settings
from my_Gift.Helper.Auth.token import get_token_for_user, verify_token
from my_Gift.Helper.Users import Users
from my_Gift.Helper.Users.Users import getUser_by_Phone, getUsers, getUser_by_Mail, getAdmin
from my_Gift.settings import IMG_URL
from my_Gift_app.Models.Users.userSerializer import UserSerializer
from my_Gift_app.Models.Users.users import User as user

@csrf_exempt
@require_http_methods(["POST"])
def Login(request):
    try:
        x = request.body

        # print(x)
        # x = json.dumps(x)

        x = json.loads(x)
        # print(x)

        PhoneNumber = x['PhoneNumber']

        password = x['password']
        # print(email)
        # print(password)

        # password = PasswordManager.encrypt(password)

        user = authenticate(PhoneNumber=PhoneNumber, password=password)
        # print(user,"User")

        if user and user.isDeleted == False and user.isActive == True:
            try:
                payload = get_token_for_user(user)
                # token = jwt.encode(payload, settings.SECRET_KEY)

                user_details = {}
                user_details['Token'] = payload['access']

                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                user_details["user"] = UserSerializer(user).data
                newData = user_details["user"]
                if (newData['profilePic'] and user.isSocial == False):
                    pp = str(IMG_URL) + "/my_Gift/uploads/" + str(newData['profilePic'])
                    newData['profilePic'] = pp

                data = newData

                user_details['user'] = data

                return JsonResponse({"data""": user_details, "status": status.HTTP_200_OK})
            except Exception as e:

                return Response({"data": str(e), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return JsonResponse({"data": res, "status": status.HTTP_403_FORBIDDEN})

    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response({"data": str(res), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CreateUserAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):

        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            if ('Id' in dic.keys()):
                if 'Id' not in dic.keys():
                    return Response(
                        {
                            'data': 'Id cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'Id is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


            profilePic = ""
            if ('profilePic' in dic.keys() and dic['isSocial'] == True):
                profilePic = dic['profilePic']

            language = ""
            if ('language' in dic.keys()):
                language = dic['language']
            Country = ""
            if ('Country' in dic.keys()):
                Country = dic['Country']
            RoleType = 2
            RoleName = "User"
            if ('RoleType' in dic.keys()):
                if (dic['RoleType'] == 0):
                    RoleName = 'Admin'
                    RoleType = 0
                elif (dic['RoleType'] == 1):
                    RoleName = 'Partner'
                    RoleType = 1

                elif (dic['RoleType'] == 2):
                    RoleName = 'User'
                    RoleType = 2

            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']

            address = ""
            if ('address' in dic.keys()):
                address = dic['address']
            isVerified = ""
            if ('isVerified' in dic.keys()):
                isVerified = dic['isVerified']
            isActive = ""
            if ('isActive' in dic.keys()):
                isActive = dic['isActive']

            if (dic['Id'] == 0 or dic['Id'] is None):
                if ('isSocial' in dic.keys()):
                        isSocial = dic['isSocial']
                else:
                    return Response(
                        {"data": "isSocial is required", "status": status.HTTP_400_BAD_REQUEST },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if ('isActive' in dic.keys()):
                        isActive = dic['isActive']
                else:
                    return Response(
                        {"data": "isActive is required it must be true", "status": status.HTTP_400_BAD_REQUEST },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if ('password' in dic.keys()):
                    if not dic['password']:
                        return Response(
                            {
                                'data': 'password cannot be empty',
                                'status': status.HTTP_400_BAD_REQUEST
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        password = dic['password']
                else:
                    return Response(
                        {"data": "password is required", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if ('UserName' in dic.keys()):
                    if not dic['UserName']:
                        return Response(
                            {"data": "UserName cannot be empty", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        UserName = dic['UserName']
                else:
                    return Response(
                        {"data": "UserName is required", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if ('Email' in dic.keys()):
                    if not dic['Email']:
                        return Response(
                            {"data": "Email cannot be empty", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        Email = dic['Email']
                else:
                    return Response(
                        {"data": "Email is required", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if ('PhoneNumber' in dic.keys()):
                    if not dic['PhoneNumber']:
                        return Response(
                            {"data": "PhoneNumber cannot be empty", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        PhoneNumber = dic['PhoneNumber']
                else:
                    return Response(
                        {"data": "Phone Number is required", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                checkUser = user.objects.filter(Email=dic["Email"], isDeleted=False).exists()
                checkphone = user.objects.filter(PhoneNumber=dic["PhoneNumber"], isDeleted=False).exists()

                if checkUser and isSocial == False:
                    return Response(
                        {"data": "User with this Email already exists", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                elif checkphone and dic['isSocial'] == False:
                    return Response(
                        {"data": "User with this Phone Number already exists", "status": status.HTTP_400_BAD_REQUEST },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif checkphone and dic['isSocial'] == True:
                    return Response(
                        {"data": "User with this Phone Number already exists", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                elif checkUser  and dic['isSocial'] == True:
                    _user = user.objects.get(Email=Email)
                    # _user.profilePic = profilePic
                    _user.isDeleted = isDeleted
                    _user.UserName = UserName
                    _user.PhoneNumber = PhoneNumber
                    _user.Country = Country
                    _user.RoleType = RoleType
                    _user.RoleName = RoleName
                    _user.address = address
                    _user.isSocial = isSocial
                    _user.isVerified = isVerified
                    _user.isActive = isActive
                    _user.language = language
                    _user.set_password(password)
                    if ("profilePic" in dic.keys()):
                        if not dic['profilePic']:
                            return Response(
                                {"data": "Please upload you profilePic ", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        if (isinstance(dic['profilePic'], str) and dic['isSocial'] == True):
                            _user.profilePic = str(dic['profilePic'])
                        elif (isinstance(dic['profilePic'], dict) and dic['isSocial'] == True):
                            return Response(
                                {"data": "you are trying to login with social Account please provide the link your image", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )


                    _user.profilePic = profilePic
                    _user.save()
                    serializer = UserSerializer(_user)
                    data = serializer.data
                    if (_user.profilePic and _user.isSocial == False):
                        pp = str(IMG_URL) + "/my_Gift/uploads/" + str(_user.profilePic)
                        data['profilePic'] = pp

                    return Response({'data':data, 'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

                else:
                    if(checkphone):
                        return Response(
                            {"data": "User with this Phone Number already exists",
                             "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    else:

                        _user = user(UserName=UserName, Email=Email, PhoneNumber=PhoneNumber,

                                     Country=Country, RoleType=RoleType, RoleName=RoleName,
                                     profilePic=profilePic, address=address,language=language,

                                     Creation_Time=datetime.datetime.now(), Deletion_Time=None, isDeleted=False,
                                     isVerified=isVerified, isSocial=isSocial,
                                     isActive=isActive,
                                     )
                        _user.set_password(password)
                        _user.save()

                        serializer = UserSerializer(_user)

                        return Response({'data':serializer.data, 'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

            else:
                _user = user.objects.get(pk=dic['Id'])


                if ("password" in dic.keys()):
                    isActive = False
                    isDeleted = False

                    _user.set_password(dic["password"])
                    if 'isActive' in dic.keys():
                        if (dic['isActive'] == True):
                            isActive = True
                            isDeleted = False
                    if 'isDeleted' in dic.keys():
                        if (dic['isDeleted'] == True):
                            isActive = False
                            isDeleted = True

                    if ("address" in dic.keys()):
                        _user.address = dic['address']
                    else:
                        _user.address = _user.address
                    if ("language" in dic.keys()):
                        _user.language = dic['language']
                    if ("Country" in dic.keys()):
                        _user.Country = dic['Country']
                    if ("UserName" in dic.keys()):
                        _user.UserName = dic['UserName']
                    if ("isSocial" in dic.keys()):
                        _user.isSocial = dic['isSocial']
                    if ("isVerified" in dic.keys()):
                        _user.isVerified = dic['isVerified']
                    email = _user.Email
                    if ('Email' in dic.keys()):
                        _user.Email = dic['Email']
                    else:
                        _user.Email=email

                    PhoneNumber = _user.PhoneNumber
                    if ('PhoneNumber' in dic.keys()):
                        _user.PhoneNumber = dic['PhoneNumber']
                    else:
                        _user.PhoneNumber = PhoneNumber

                    if ("profilePic" in dic.keys()):
                        if not dic['profilePic']:
                            return Response(
                                {"data": "its cannot be empty Please upload you profilePic", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        if (isinstance(dic['profilePic'], str) and dic['isSocial'] == True):
                            _user.profilePic = str(dic['profilePic'])
                        elif (isinstance(dic['profilePic'], dict)and dic['isSocial'] == True):
                            return Response(
                                {"data": "you are not login with social Account please provide the link your image", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        elif (isinstance(dic['profilePic'], str) and dic['isSocial'] == False):
                            return Response(
                                {"data": "you are not login with social account please upload your profile picture", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        elif (isinstance(dic['profilePic'], dict)):
                          if ("fileName" in dic["profilePic"].keys()):
                            url = dic['profilePic']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + dic['profilePic'][
                                'fileName']
                            filename = str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()

                                if (_user.profilePic):
                                    if os.path.exists(str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + _user.profilePic):
                                        os.remove(str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + _user.profilePic)

                                _user.profilePic = name

                    _user.isActive = isActive
                    # _user.isSocial = dic["isSocial"]
                    # _user.address = dic["address"]
                    _user.isDeleted = isDeleted
                    _user.set_password(dic['password'])


                    _user.save()
                    serializer = UserSerializer(_user)
                    newData = serializer.data
                    if (_user.profilePic and _user.isSocial == False):
                        pp = str(IMG_URL) + "/my_Gift/uploads/" + str(_user.profilePic)
                        newData['profilePic'] = pp
                    else:
                        pass
                    return Response({"data": newData, "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)


                else:

                    isActive = False
                    isDeleted = False

                    if 'isActive' in dic.keys():
                        if (dic['isActive'] == True):
                            isActive = True
                            isDeleted = False
                    if 'isDeleted' in dic.keys():
                        if (dic['isDeleted'] == True):
                            isActive = False
                            isDeleted = True
                    if ("address" in dic.keys()):
                        _user.address = dic['address']

                    if ("language" in dic.keys()):
                        _user.language = dic['language']
                    if ("Country" in dic.keys()):
                        _user.Country = dic['Country']
                    if ("UserName" in dic.keys()):
                        _user.UserName = dic['UserName']
                    if ("PhoneNumber" in dic.keys()):
                        _user.PhoneNumber = dic['PhoneNumber']
                    if ("Email" in dic.keys()):
                        _user.Email = dic['Email']
                    isSocial = ''
                    if ('isSocial' in dic.keys()):
                        _user.isSocial = dic['isSocial']
                    isVerified = ''
                    if ('isVerified' in dic.keys()):
                        _user.isVerified = dic['isVerified']


                    if ("profilePic" in dic.keys()):
                        if not dic['profilePic']:
                            return Response(
                                {"data": "it cannot be empty Please upload you profilePic", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        if (isinstance(dic['profilePic'],str) and dic['isSocial'] == True):
                            _user.profilePic = str(dic['profilePic'])
                        elif (isinstance(dic['profilePic'],dict) and dic['isSocial'] == True):
                            return Response(
                                {"data": "you are trying to login with social accounts please provide link of profille picture", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        elif (isinstance(dic['profilePic'], str)and dic['isSocial'] == False):
                            return Response(
                                {"data": "you are not login with social account please upload your profile picture", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        elif (isinstance(dic['profilePic'], dict)):
                            if ("fileName" in dic["profilePic"].keys()):
                                url = dic['profilePic']["filePath"]
                                url = url.split(",")
                                filedata = base64.b64decode(url[1])
                                name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + dic['profilePic'][
                                    'fileName']
                                filename = str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + name
                                with open(filename, 'wb') as f:
                                    f.write(filedata)
                                    f.close()
                                    if (_user.profilePic):
                                        if os.path.exists(
                                                str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + _user.profilePic):
                                            os.remove(str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + _user.profilePic)
                                            # from urllib.request import urlopen
                                            # url='http://localhost:8001/my_Gift/uploads/'+filename
                                            # response = urlopen(url)
                                    _user.profilePic = name

                    _user.isActive = isActive
                    # _user.address = dic["address"]
                    # _user.isSocial = dic["isSocial"]
                    _user.isDeleted = isDeleted

                    _user.save()
                    serializer = UserSerializer(_user)
                    newData = serializer.data
                    if (_user.profilePic and _user.isSocial == False):
                        pp = str(IMG_URL) + "/my_Gift/uploads/" + str(_user.profilePic)
                        newData['profilePic'] = pp

                    return Response({"data": newData, "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserRetrieveAPIView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            users = getUsers()
            data = []
            for user in users:
                serializer = self.serializer_class(user)
                newData = serializer.data
                if (user.profilePic and user.isSocial == False):
                    pp = str(IMG_URL) + "/my_Gift/uploads/" + str(user.profilePic)
                    newData['profilePic'] = pp
                data.append(newData)

            # print(serializer.data)
            return Response({"data": data, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            user = Users.getUser_by_Id(pk)
            if (user is None):
                return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(user)
            newData = serializer.data
            if (user.profilePic and user.isSocial == False):
                pp = str(IMG_URL) + "/my_Gift/uploads/" + str(user.profilePic)
                newData['profilePic'] = pp

            return Response(newData, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request, *args, **kwargs):
        try:
            d = request.data
            if ('Email' in d.keys()):
                Email = d['Email']
            else:
                return Response(
                    {"data": "Email is required", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = getUser_by_Mail(d['Email'])
            if user is None:
                return Response({"data": "User doesn't exists", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(user)
            newData = serializer.data
            if (user.profilePic and user.isSocial == False):
                pp = str(IMG_URL) + "/my_Gift/uploads/" + str(user.profilePic)
                newData['profilePic'] = pp

            # print(serializer.data)
            return Response({"data": newData, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request, *args, **kwargs):
        try:
            d = request.data
            if ('PhoneNumber' in d.keys()):
                PhoneNumber = d['PhoneNumber']
            else:
                return Response(
                    {"data": "PhoneNumber is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user = getUser_by_Phone(d['PhoneNumber'])
            if user is None:
                return Response({"data": "User doesn't exists", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(user)
            newData = serializer.data
            if (user.profilePic and user.isSocial == False):
                pp = str(IMG_URL) + "/my_Gift/uploads/" + str(user.profilePic)
                newData['profilePic'] = pp

            # print(serializer.data)
            return Response({"data": newData, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            # serializer to handle turning our `User` object into something that
            # can be JSONified and sent to the client.
            # print(request.user)
            users = getAdmin()
            data = []
            for user in users:
                serializer = self.serializer_class(user)
                newData = serializer.data
                if (user.profilePic and user.isSocial == False):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(user.profilePic)
                    newData['profilePic'] = pp
                data.append(newData)

            # print(serializer.data)
            return Response({"data": data, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TokenVerify(TokenViewBase):
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        return verify_token(request)