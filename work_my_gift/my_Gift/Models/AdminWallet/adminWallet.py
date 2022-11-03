import datetime
import json

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift.Helper.AdminWalletHelper.adminWalletHelper import get_admin_wallet_Id, Admin_Wallet_by_Id
from my_Gift.Helper.Users.Users import getAdmin, getUser_by_Id
from my_Gift_app.Models.AdminWallet.adminWallet import AdminWallet
from my_Gift_app.Models.Nitifications.notifications import Notifications
from my_Gift_app.Models.Transactions.transactions import Transactions


class AdminWalletListUpdateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            wallet = Admin_Wallet_by_Id()
            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']
            if ('balance' in dic.keys()):
                balance = dic['balance']
            else:
                return Response(
                    {"data": "Balance is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            userId = ''
            if ('userId' in dic.keys()):
                if not dic['userId']:
                    return Response(
                        {
                            'data': 'userId of sender cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    userId = dic['userId']
            else:
                return Response(
                    {"data": "userId of sender is required", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = getUser_by_Id(userId)
            if wallet is None:
                AD_wallet = AdminWallet(

                    balance=balance,
                    isDeleted=isDeleted,

                )
                AD_wallet.save()
                Admins = getAdmin()
                for admin in Admins:
                    notification = Notifications(
                        notification_by=user,
                        notification_to=admin,
                        description=AdminWallet.balance + " has been added to your account"
                    )
                    notification.save()
                trans = Transactions(
                    currency="SAR",
                    status_code=0,
                    status_message="Paid",
                    payment_type="Admin_receive",
                    sent_by=user,
                    creation_time=datetime.datetime.now()
                )
                trans.save()

                data = model_to_dict(AD_wallet)

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

            else:

                wallet.balance =  str(float( wallet.balance ) + float(balance))
                wallet.isDeleted = isDeleted
                wallet.save()
                Admins = getAdmin()
                for admin in Admins:
                    notification = Notifications(
                        notification_by=user,
                        notification_to=admin,
                        description=str(dic['balance'])+ " SAR has been added to your account "
                    )
                    notification.save()

                trans = Transactions(
                    currency="SAR",
                    status_code=0,
                    status_message="Paid",
                    payment_type="Admin_receive",
                    sent_by=user,
                    creation_time=datetime.datetime.now()
                )
                trans.save()

                data = model_to_dict(wallet)

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            # print(ex)
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, *args, **kwargs):
        try:
            dic = request.data
            wallet = Admin_Wallet_by_Id()
            userId = ''
            if ('userId' in dic.keys()):
                if not dic['userId']:
                    return Response(
                        {
                            'data': 'userId of sender cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    userId = dic['userId']
            else:
                return Response(
                    {"data": "userId of sender is required", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = getUser_by_Id(userId)
            if ('balance' in dic.keys()):
                balance = dic['balance']
            else:
                return Response(
                    {"data": "Balance is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']
            if (wallet is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                if (float(wallet.balance) < float(dic['balance'])):
                    return Response({"data": "you don't have enough money",
                                     "status": status.HTTP_400_BAD_REQUEST},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    wallet.balance = str(float(wallet.balance) - float(balance))
                    wallet.isDeleted = isDeleted
                    wallet.save()
                    Admins = getAdmin()
                    for admin in Admins:
                        notification = Notifications(
                            notification_by=request.user,
                            notification_to=admin,
                            description=str(dic['balance']) + "SAR has been deducted from your account"
                        )
                        notification.save()

                    trans = Transactions(
                        currency="SAR",
                        status_code=0,
                        status_message="Paid",
                        payment_type="Admin_send",
                        sent_by=user,
                        creation_time=datetime.datetime.now()
                    )
                    trans.save()
                    data = model_to_dict(wallet)




                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk):
        try:
            data = []
            wallet = get_admin_wallet_Id(pk)
            if(wallet is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},status=status.HTTP_404_NOT_FOUND)
            else:

                data = model_to_dict(wallet)


            return Response({"data": data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},status=status.HTTP_500_INTERNAL_SERVER_ERROR)