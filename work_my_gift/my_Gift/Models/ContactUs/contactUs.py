import json
import threading

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift import settings
from my_Gift.Helper.ContactUsHelper.contactUsHelper import get_all_contact, contact_us_by_Id
from my_Gift.Helper.EmailHelper import emailHelper
from my_Gift_app.Models.ContactUs.contactUs import ContactUs


class ContactUsListUpdate(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,*args, **kwargs):
        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            # contact = contact_us_by_Id(dic['Id'])
            if "name" in dic.keys():
                name = dic['name']
                if not dic['name']:
                    return Response(
                        {"data": "Name cannot be empty"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"data": "Name is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            if 'phoneNumber' in dic.keys():
                phoneNumber = dic['phoneNumber']
                if not dic['phoneNumber']:
                    return Response(
                        {"data": "phoneNumber cannot be empty"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"data": "phoneNumber is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'message' in dic.keys():
                message = dic['message']
                if not dic['message']:
                    return Response(
                        {"data": "message cannot be empty"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"data": "message is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']


            # if contact is None:
            con = ContactUs(

                    name=name,
                    email=email,
                    phoneNumber=phoneNumber,
                    message=message,
                    isDeleted=isDeleted

                )
            con.save()
            body = "We appreciate you contacting us " + con.name + ".One of our members will be getting back to you shortly. <br/><br/>"

            t = threading.Thread(target=emailHelper.send_Mail,
                                     args=("Contact MyGift", body, con.name, con.email))
            t.setDaemon(True)
            t.start()
            body2 = "MyGift User : <b>" + con.name + "</b>.sent a message having phone number <b>" + con.phoneNumber + "</b> , Email <b>" + con.email + "</b> and message <b>" + con.message + "</b>. <br/><br/>"

            t2 = threading.Thread(target=emailHelper.send_Mail,
                                  args=("Contact Us", body2, settings.EMAIL_HOST_NAME, settings.EMAIL_HOST_USER))
            t2.setDaemon(True)
            t2.start()

            cont = model_to_dict(con)
            return JsonResponse({"data": cont, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, *args, **kwargs):
        try:
            data = []
            contact = contact_us_by_Id(pk)
            if (contact is None):
                return JsonResponse({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(contact)

                return JsonResponse({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            contacts = get_all_contact()
            if (contacts is None):
                return JsonResponse({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                for cons in contacts:
                    con_data = model_to_dict(cons)
                    data.append(con_data)


                return JsonResponse({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)