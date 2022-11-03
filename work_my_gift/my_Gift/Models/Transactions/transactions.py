from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift.Helper.CardsHelper.cardsHelper import getCard_by_Id
from my_Gift.Helper.TransactionsHelper.transactionsHelper import get_transaction_by_User_Id, get_transaction_by_Id, \
    getAllTransactions, get_Admin_Transactions_Receive, get_Admin_Transactions_send, get_all_Admin_Transactions, \
    get_Admin_Transactions_card, get_User_Transactions_Card, get_User_Wallet_Transactions, \
    get_User_withdraw_Transactions, get_all_User_Transactions, get_Partner_Wallet_Transactions, \
    get_partner_withdraw_Transactions, get_all_Partner_Transactions
from my_Gift.Helper.Users.Users import getUser_by_Id
from my_Gift.Helper.imgurlhelper.urlhelper import img_url_profile
from my_Gift.settings import IMG_URL
from my_Gift_app.Models.Transactions.transactions import Transactions
from my_Gift_app.Models.Users.userSerializer import UserSerializer


class TransactionsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            d = request.data
            if ('Id' in d.keys()):
                if 'Id' not in d.keys():
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
            user = None
            card = None
            if ('sent_by' in d.keys()):
                user = getUser_by_Id(d['sent_by'])
                if (user is None):
                    return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
            if ('card_id' in d.keys()):
                card = getCard_by_Id(d['card_id'])
                if (card is None):
                    return Response({"data": "card doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)

            # if (trans is None):
            #     return Response({"data": "Transaction doesn't exists", "status": status.HTTP_404_NOT_FOUND},
            #                     status=status.HTTP_404_NOT_FOUND)
            cart_id = ""
            if ('cart_id' in d.keys()):
                cart_id = d['cart_id']
            amount = 0
            if ('amount' in d.keys()):
                amount = d['amount']
            currency = "SAR"
            if ('currency' in d.keys()):
                currency = d['currency']
            country = ""
            if ('country' in d.keys()):
                country = d['country']
            address = ""
            if ('address' in d.keys()):
                address = d['address']
            order_ref = ""
            if ('order_ref' in d.keys()):
                order_ref = d['order_ref']
            status_code = ""
            if ('status_code' in d.keys()):
                status_code = d['status_code']
            status_message = ""
            if ('status_message' in d.keys()):
                status_message = d['status_message']

            sent_to = ""
            if ('sent_to' in d.keys()):
                sent_to = d['sent_to']
            customer_name = ""
            if ('customer_name' in d.keys()):
                customer_name = d['customer_name']
            customer_email = ""
            if ('customer_email' in d.keys()):
                customer_email = d['customer_email']
            description = ""
            if ('description' in d.keys()):
                description = d['description']
            IBAN = ""
            if ('IBAN' in d.keys()):
                IBAN = d['IBAN']
            purpose = ""
            if ('purpose' in d.keys()):
                purpose = d['purpose']
            isDeleted = False
            if ('isDeleted' in d.keys()):
                isDeleted = d['isDeleted']
            payment_type = ""
            if user.RoleType == 0 and IBAN:
                payment_type = 'Admin_send'

            if user.RoleType == 0 and cart_id:
                payment_type = "Admin_card"
            if user.RoleType == 1 and IBAN:
                payment_type = 'partner_withdrawal'

            if user.RoleType == 1 and cart_id:
                payment_type = "partner_card_paid"

            if user.RoleType == 2 and IBAN:
                payment_type = 'user_withdrawal'

            if user.RoleType == 2 and cart_id:
                payment_type = "Gift_Card"

            if "payment_type" in d.keys():
                payment_type = d['payment_type']


            check = False
            if ('Id' in d.keys()):

                if (d['Id'] == 0 or d['Id'] == None):
                    check = True
                else:
                    check = False
            else:
                check = False
            if (check):
                trans = Transactions(
                    cart_id=cart_id,
                    amount=amount,
                    currency=currency,
                    country=country,
                    address=address,
                    order_ref=order_ref,
                    status_code=status_code,
                    status_message=status_message,
                    payment_type=payment_type,
                    sent_to=sent_to,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    description=description,
                    IBAN=IBAN,
                    purpose=purpose,
                    isDeleted=isDeleted
                )
                if (user is not None):
                    trans.sent_by = user
                if (card is not None):
                    trans.card_id = card

                trans.save()

                data = model_to_dict(trans)

                if (trans.card_id):
                    data['card_id'] = model_to_dict(trans.card_id)

                if (trans.sent_by):
                    data['sent_by'] = (UserSerializer(trans.sent_by)).data
                    if (trans.sent_by.profilePic):
                        data['sent_by']['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(
                            trans.sent_by.profilePic)
                for d in data.keys():
                    if (data[d] is None):
                        data[d] = ""
                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
            else:
                trans = Transactions.objects.get(pk=d['Id'])
                if (cart_id):
                    trans.cart_id = cart_id
                if (amount):
                    trans.amount = amount
                if (currency):
                    trans.currency = currency
                if (country):
                    trans.country = country
                if (address):
                    trans.address = address
                if (order_ref):
                    trans.order_ref = order_ref
                if (status_code):
                    trans.status_code = status_code
                if (status_message):
                    trans.status_message = status_message
                if user.RoleType == 0 and IBAN:
                    payment_type = 'Admin_send'

                if user.RoleType == 0 and cart_id:
                    payment_type = "Admin_card"
                if user.RoleType == 1 and IBAN:
                    payment_type = 'partner_withdrawal'

                if user.RoleType == 1 and cart_id:
                    payment_type = "partner_card_paid"

                if user.RoleType == 2 and IBAN:
                    payment_type = 'user_withdrawal'

                if user.RoleType == 2 and cart_id:
                    payment_type = "Gift_Card"
                if (payment_type):
                    trans.payment_type = payment_type
                if (sent_to):
                    trans.sent_to = sent_to
                if (customer_name):
                    trans.customer_name = customer_name
                if (customer_email):
                    trans.customer_email = customer_email
                if (description):
                    trans.description = description
                if (IBAN):
                    trans.IBAN = IBAN
                if (purpose):
                    trans.purpose = purpose
                if (isDeleted):
                    trans.isDeleted = isDeleted

                if (user is not None):
                    trans.sent_by = user
                if (card is not None):
                    trans.card_id = card

                trans.save()

                data = model_to_dict(trans)
                if (trans.card_id):
                    data['card_id'] = model_to_dict(trans.card_id)
                if (trans.sent_by):
                    data['sent_by'] = (UserSerializer(trans.sent_by)).data
                    if (trans.sent_by.profilePic):
                        data['sent_by']['profilePic'] = str(IMG_URL) + "/myGift/uploads/" + str(
                            trans.sent_by.profilePic)
                for d in data.keys():
                    if (data[d] is None):
                        data[d] = ""
                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)



        except Exception as ex:
            # print(ex)

            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def get(self, request, *args, **kwargs):
        try:
            data = []
            list = {}
            transaction = get_all_Admin_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)
                list.update({"Admin": data})

            users = get_all_Partner_Transactions()
            for trans in users:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)
                list.update({"Partner": data})

            users = get_all_User_Transactions()
            for trans in users:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)
                list.update({"Users": data})

            return Response({"data": list, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def put(self, request, pk, format=None):

        try:
            data = {}
            trans = get_transaction_by_Id(pk)
            if (trans is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(trans)

                # data['card_id'] = model_to_dict(trans.card_id)
                data['sent_by'] = (UserSerializer(trans.sent_by)).data
                if (trans.sent_by.profilePic):
                    data['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for d in data.keys():
                    if (data[d] is None):
                        data[d] = ""
                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionsByUserIdUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:

            data = []
            transactions = get_transaction_by_User_Id(pk)
            if (transactions is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            for trans in transactions:
                transData = model_to_dict(trans)
                if (transData['card_id'] is not None):
                    transData['card_id'] = model_to_dict(trans.card_id)
                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (transData['sent_to'] is not None):
                    transData['sent_to'] = UserSerializer(getUser_by_Id(transData['sent_to'])).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for t in transData.keys():
                    if (transData[t] is None):
                        transData[t] = ""
                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminTransactionsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_Admin_Transactions_Receive()
            for trans in transaction:
                transData = model_to_dict(trans)

                # transData['card_id'] = model_to_dict(trans.card_id)
                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def put(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_Admin_Transactions_send()
            for trans in transaction:
                transData = model_to_dict(trans)

                # transData['card_id'] = model_to_dict(trans.card_id)
                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def patch(self, request, *args, **kwargs):
        try:
            data = []

            transaction = get_all_Admin_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                # transData['card_id'] = model_to_dict(trans.card_id)
                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

class AdminCardTransactionsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_Admin_Transactions_card()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

class PartnerTransactionsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_Partner_Wallet_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def put(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_partner_withdraw_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def patch(self, request, *args, **kwargs):
        try:
            data = []

            transaction = get_all_Partner_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})


class UserTransactionsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_User_Transactions_Card()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def put(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_User_Wallet_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def patch(self, request, *args, **kwargs):
        try:
            data = []

            transaction = get_User_withdraw_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

class UserAllTransactionsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            transaction = get_all_User_Transactions()
            for trans in transaction:
                transData = model_to_dict(trans)

                transData['sent_by'] = UserSerializer(trans.sent_by).data
                if (trans.sent_by.profilePic):
                    transData['sent_by']['profilePic'] = img_url_profile(trans.sent_by.profilePic)
                for trans in transData.keys():
                    if (transData[trans] is None):
                        transData[trans] = ""

                data.append(transData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})