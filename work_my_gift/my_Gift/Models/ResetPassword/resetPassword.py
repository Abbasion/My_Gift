import datetime
import json
import threading

from django.http import HttpResponse, JsonResponse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from my_Gift import settings
from my_Gift.Helper.EmailHelper import emailHelper
from my_Gift.Helper.EmailHelper.emailHelper import account_activation_token
from my_Gift.Helper.Users.Users import getUser_by_Mail
from my_Gift.settings import IMG_URL
from my_Gift_app.Models.Users.userSerializer import UserSerializer
from my_Gift_app.Models.Users.users import User


class Forget_password(APIView):
    def post(self, request, format=None):
        try:
            dic = request.data
            # dic = json.dumps(data)
            # dic = json.loads(dic)
            if "email" in dic.keys():
                email = dic['email']
                if not dic['email']:
                    return Response(
                        {"data": "email cannot be empty"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"data": "email is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = getUser_by_Mail(dic['email'])
            if user is None:
                return Response(
                    {"data": "user doesn't exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            print(user.Id)
            if (user is not None):
                user.isActive = False
                user.save()
                uid = urlsafe_base64_encode(force_bytes(user.Id))
                token =account_activation_token.make_token(user)
                link = settings.client + uid + '/' + token
                body = "Please click on the link to reset your password, <br/><br/>" \
                       "<a href=" + link + " target='_blank' style='background:#E84E22;border-radius:15px; width:100%; padding:10px;text-decoration:none;margin:5px auto; color:white'>RESET</a> \
                <br/>"
                t = threading.Thread(target=emailHelper.send_Mail,
                                     args=("Password Reset", body,user.UserName, user.Email))
                t.setDaemon(True)
                t.start()
                # data = {
                #     'subject': 'Reset Your Password',
                #     'body': body,
                #     'to_email': user.Email,
                #     'from_email':settings.EMAIL_HOST_USER
                # }
                # EmailHelper.send_Mail(data)
                # user.save()
                return JsonResponse({"data": "Email has been sent Please Check your inbox", "Status": status.HTTP_200_OK})

            else:
                return JsonResponse({"data": "User doesn't exist", "Status": status.HTTP_404_NOT_FOUND})
        except Exception as ex:
            return JsonResponse({"data": str(ex), "Status": status.HTTP_200_OK})


@permission_classes(AllowAny)
def resendActivationLink(request,uid):
    try:
        _user =getUser_by_Mail(uid)
        _user.Creation_Time = datetime.datetime.now()
        userId = urlsafe_base64_encode(force_bytes(_user.Id))
        token =account_activation_token.make_token(_user)
        _user.isActive=False
        _user.save()
        url = settings.client  + userId + "/" + token
        txt =' <span style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>\
                                        <p style="color:#455056; font-size:15px;line-height:24px; margin:0;">\
                                            You recently requested to reset your password for your MyGift account.\
                                            We cannot simply send you your old password. A unique link to reset your\
                                            password has been generated for you. To reset your password, click the\
                                            following link and follow the instructions.\
                                        </p>\
                                        <a target="_blank" href='+url+'\
                                            style="background:#20e277;text-decoration:none !important; font-weight:500; margin-top:35px; color:#fff;text-transform:uppercase; font-size:14px;padding:10px 24px;display:inline-block;border-radius:50px;">Reset\
                                            Password</a>'
        emailHelper.send_Mail("Activate your account", txt, _user.UserName + ",<br/>You have\
                                            requested to reset your password", _user.Email)
        return HttpResponse(json.dumps({"data": "Email has been Re-send please check your inbox","status": status.HTTP_200_OK}),
                            status=status.HTTP_200_OK, content_type='application/json')

    except Exception as ex:
        print(ex)
        return HttpResponse(json.dumps({"status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION}),
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content_type='application/json')




def Reset(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as ex:
            print(ex)
            user = None
        checkToken = account_activation_token.check_token(user, token)
        if user is not None and checkToken and user.isActive == False:
            user.isActive = True
            user.isSocial = False
            user.save()
            serializer = UserSerializer(user)
            newData = serializer.data
            if (user.profilePic):
                newData['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(user.profilePic)
            return HttpResponse(json.dumps(
                {"data": 'Thank you for your email confirmation. Now you can login your account.', "user": newData,
                 "status": status.HTTP_200_OK}), status=status.HTTP_200_OK, content_type='application/json')
        else:
            return HttpResponse(json.dumps(
                {"data": 'Activation link is invalid!', "status": status.HTTP_203_NON_AUTHORITATIVE_INFORMATION}),
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content_type='application/json')
