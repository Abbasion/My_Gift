from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift.Helper.NotificationsHelper.notificationsHelper import get_notification_by_User_Id, get_notification_by_Id
from my_Gift.Helper.Users.Users import getUser_by_Id
from my_Gift.Helper.imgurlhelper.urlhelper import img_url_profile
from my_Gift_app.Models.Nitifications.notifications import Notifications
from my_Gift_app.Models.Users.userSerializer import UserSerializer


class NotificationListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            dic=request.data
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

            if ('notification_by' in dic.keys()):
                notification_by = dic['notification_by']
                if not dic['notification_by']:
                    return Response(
                        {
                            'data': 'notification_by cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'notification_by is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if ('notification_to' in dic.keys()):
                notification_to = dic['notification_to']
                if not dic['notification_to']:
                    return Response(
                        {
                            'data': 'notification_to cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'notification_to is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            if ('description' in dic.keys()):
                description = dic['description']
                if not dic['description']:
                    return Response(
                        {
                            'data': 'description cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'description is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user=getUser_by_Id(notification_by)
            if (dic['Id'] == 0 or dic['Id'] == None):
                noti = Notifications(
                    notification_by= user,
                    notification_to = notification_to,
                    description = description

                )
                noti.save()
                data = model_to_dict(noti)
                data['notification_by'] = (UserSerializer(noti.notification_by)).data
                if (noti.notification_by.profilePic):
                    data['notification_by']['profilePic'] =img_url_profile(noti.notification_by.profilePic)
            return Response({"data": data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk):
        try:
            data = []
            notification = get_notification_by_Id(pk)
            if(notification is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},status=status.HTTP_404_NOT_FOUND)
            else:

                data = model_to_dict(notification)
                data['notification_by'] = UserSerializer(notification.notification_by).data

                if (notification.notification_by.profilePic):
                    data['notification_by']['profilePic'] =img_url_profile(notification.notification_by.profilePic)




                return Response({"data": data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk, format=None):
        try:

            data = []
            notification = get_notification_by_User_Id(pk)
            for noti in notification:
                N_Data = model_to_dict(noti)
                N_Data['notification_by'] = UserSerializer(noti.notification_by).data
                if (noti.notification_by.profilePic):
                    N_Data['notification_by']['profilePic'] = img_url_profile(noti.notification_by.profilePic)
                data.append(N_Data)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)