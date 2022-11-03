from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift.Helper.Users.Users import getAdmin
from my_Gift.Helper.imgurlhelper.urlhelper import img_url_profile
from my_Gift_app.Models.Transactions.transactions import Transactions
from my_Gift_app.Models.Users.userSerializer import UserSerializer


class WidthDrawalAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            dic = request.data

            order_ref = ""
            if ('order_ref' in dic.keys()):
                order_ref = dic['order_ref']
            cart_id = ""
            if ('cart_id' in dic.keys()):
                cart_id = dic['cart_id']
            amount = ""
            if ('amount' in dic.keys()):
                amount = dic['amount']
                if not dic['amount']:
                    return Response(
                        {
                            'data': 'amount cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'amount is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            currency = ""
            if ('currency' in dic.keys()):
                currency = dic['currency']
            status_code = ""
            if ('status_code' in dic.keys()):
                status_code = dic['status_code']
                if not dic['status_code']:
                    return Response(
                        {
                            'data': 'status_code cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'status_code is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            status_message = ""
            if ('status_message' in dic.keys()):
                status_message = dic['status_message']

            status_message = ""
            if ('status_message' in dic.keys()):
                status_message = dic['status_message']


            sent_by = ""
            if ('sent_by' in dic.keys()):
                sent_by = dic['sent_by']
            sent_to = ""
            if ('sent_to' in dic.keys()):
                sent_to = dic['sent_to']
            customer_name = ""
            if ('customer_name' in dic.keys()):
                customer_name = dic['customer_name']
            customer_email = ""
            if ('customer_email' in dic.keys()):
                customer_email = dic['customer_email']
            description = ""
            if ('description' in dic.keys()):
                description = dic['description']

            card_id = ""
            if ('card_id' in dic.keys()):
                card_id = dic['card_id']

            IBAN = ""
            if ('IBAN' in dic.keys()):
                IBAN = dic['IBAN']
            purpose = ""
            if ('purpose' in dic.keys()):
                purpose = dic['purpose']
            country = ""
            if ('country' in dic.keys()):
                country = dic['country']
            address = ""
            if ('address' in dic.keys()):
                address = dic['address']

            user = request.user
            payment_type = ""
            if user.RoleType == 0 and IBAN:
                payment_type='Admin_send'

            if user.RoleType == 0 and cart_id:
                payment_type = "Admin_card"
            if user.RoleType == 1 and IBAN:
                payment_type='partner_withdrawal'

            if user.RoleType == 1 and cart_id:
                payment_type = "partner_card_paid"

            if user.RoleType == 2 and IBAN:
                payment_type='user_withdrawal'

            if user.RoleType == 2 and cart_id:
                payment_type = "Gift_Card"

            if "payment_type" in dic.keys():
                payment_type = dic['payment_type']
            # user = getUser_by_Id(dic['sent_by'])

            # card = getCard_by_Id(dic['card_id'])
            Admins = getAdmin()
            trans = Transactions(
                cart_id=cart_id,
                order_ref=order_ref,
                amount=amount,
                currency=currency,
                status_code=status_code,
                status_message=status_message,
                payment_type=payment_type,
                sent_by=user,
                sent_to=Admins[0].Id,
                customer_name=customer_name,
                customer_email=customer_email,
                description=description,

                IBAN=IBAN,
                purpose=purpose,
                country=country,
                address=address,
                # creation_time=datetime.datetime.now()
            )
            trans.save()
            data = model_to_dict(trans)

            data['sent_by'] = UserSerializer(trans.sent_by).data
            if (trans.sent_by.profilePic):
                data['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})