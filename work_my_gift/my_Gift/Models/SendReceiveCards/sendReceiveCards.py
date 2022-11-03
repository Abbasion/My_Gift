import base64
import datetime
import math
import os

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift import settings
from my_Gift.Helper.CardsHelper.cardsHelper import getCard_by_Id, generateCartId
from my_Gift.Helper.SendReceiveCardsHelper.sendReceiveCardsHelper import getReceive_by_Phonenumber, getAllSendCard, \
    getReceiveCard_by_Id, getSendCard_by_UserId, getAllClamiedSendCard, getReceiveCard_by_Phonenumber, \
    Clamied_Card_by_UserId
from my_Gift.Helper.Users.Users import getUser_by_Id, getUser_by_Ph
from my_Gift.Helper.imgurlhelper.urlhelper import img_url_profile, img_url
from my_Gift.settings import IMG_URL
from my_Gift_app.Models.Nitifications.notifications import Notifications
from my_Gift_app.Models.SendReceiveCards.sendReceiveCards import SendReceiveCards
from my_Gift_app.Models.Transactions.transactions import Transactions
from my_Gift_app.Models.Users.userSerializer import UserSerializer


class SendReceiveCardsUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk, format=None):

        try:
            data = []
            card = getReceiveCard_by_Id(pk)
            if (card is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(card)
                data['card'] = model_to_dict(card.card)
                if (data['cardPic']):
                    data['cardPic'] = img_url(data['cardPic'])
                data['senderId'] = (UserSerializer(card.senderId)).data
                if (card.senderId.profilePic):
                    data['senderId']['profilePic'] = img_url_profile(card.senderId.profilePic)
                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:

            data = []

            cards = getAllSendCard()
            if (cards is None):
                return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            for card in cards:
                cardData = model_to_dict(card)
                cardData['card'] = model_to_dict(card.card)

                if (card.cardPic):
                    cardData['cardPic'] = img_url(card.cardPic)
                cardData['senderId'] = UserSerializer(card.senderId).data
                if (card.senderId.profilePic):
                    cardData['senderId']['profilePic'] = img_url_profile(card.senderId.profilePic)
                data.append(cardData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

    def post(self, request):
        try:
            d = request.data
            # d = json.loads(data)
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




            if ('receiverPhone' in d.keys()):
                receiverPhone = d['receiverPhone']
                if not d['receiverPhone']:
                    return Response(
                        {
                            'data': 'receiverPhone cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'receiverPhone is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            card = ''
            if 'card' in d.keys():
                card = d['card']
                if not d['card']:
                    return Response(
                        {
                            'data': 'card Id cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {
                        'data': 'card Id is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            notification_to = getReceive_by_Phonenumber(d['receiverPhone'])
            user = request.user #getUser_by_Id(d['senderId'])
            if (user is None):
                return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)

            card = getCard_by_Id(d['card'])
            if (card is None):
                return Response({"data": "card doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            # _card =SendReceiveCards.objects.get(pk=d['Id'])

            if (d['Id'] == 0 or d['Id'] == None):
                isClaimed = False
                if 'isClaimed' in d.keys():
                    isClaimed = d['isClaimed']
                description = ''
                if "description" in d.keys():
                    description = d['description']
                recieverName = ''
                if 'recieverName' in d.keys():
                    recieverName = d['recieverName']
                    if not d['recieverName']:
                        return Response(
                            {
                                'data': 'recieverName cannot be empty',
                                'status': status.HTTP_400_BAD_REQUEST
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                else:
                    return Response(
                        {
                            'data': 'recieverName Id is required',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                isDeleted = False
                if 'isDeleted' in d.keys():
                    isDeleted = d['isDeleted']
                send = SendReceiveCards(
                    senderId=user,
                    card=card,
                    receiverPhone=receiverPhone,
                    isClaimed=isClaimed,
                    description=description,
                    recieverName=recieverName,
                    isDeleted=isDeleted,

                )
                if ("cardPic" in d.keys()):
                    if not d['cardPic']:
                        return Response(
                            {"data": "Please upload you cardPic its cannot be empty!", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if (isinstance(d['cardPic'], str)):
                        return Response(
                            {"data": "Please upload you cardPic, it cannot be string", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    elif (isinstance(d['cardPic'], dict)):
                        if ("fileName" in d["cardPic"].keys()):
                            url = d['cardPic']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + d['cardPic'][
                                'fileName']
                            filename = str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()

                                send.cardPic = name

                send.save()
                cart_id = generateCartId(card, user.Id)

                if (notification_to is None):
                    pass
                else:
                    notification = Notifications(
                        notification_by=user,
                        notification_to=str(notification_to.Id),
                        description="you send a card to  " + notification_to.UserName
                    )
                    notification.save()
                if (notification_to is None):
                    pass
                else:
                    trans = Transactions(
                        cart_id=cart_id,
                        amount=card.amount,
                        currency="SAR",
                        status_code=0,
                        status_message="Paid",
                        payment_type="Gift_Card",
                        sent_by=user,
                        sent_to=notification_to.Id,
                        card_id=card,
                        creation_time=datetime.datetime.now()
                    )
                    trans.save()

                data = model_to_dict(send)
                data['card'] = model_to_dict(send.card)
                data['senderId'] = (UserSerializer(send.senderId)).data
                if (send.senderId.profilePic):
                    data['senderId']['profilePic'] = str(IMG_URL) + "/my_Gift/uploads/" + str(send.senderId.profilePic)
                newData = model_to_dict(send)
                newData['senderId'] = (UserSerializer(send.senderId)).data
                if (send.cardPic):
                    pp = str(IMG_URL) + "/my_Gift/uploads/" + str(name)
                    newData['cardPic'] = pp

                return Response({"data": newData,"cart_Id":cart_id, "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
            else:
                sentCard = SendReceiveCards.objects.get(pk=d['Id'])
                if (sentCard is None):
                    return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
                sentCard.senderId = user
                if (sentCard.senderId is None):
                    return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
                if 'isDeletted' in d.keys():
                    sentCard.isDeleted = d['isDeleted']
                sentCard.card = card
                sentCard.receiverPhone = receiverPhone
                if 'description' in d.keys():
                    sentCard.description = d['description']
                isClaimed = False
                if 'isClaimed' in d.keys():
                    sentCard.isClaimed = d['isClaimed']
                else:
                    return Response(
                        {"data": "isClaimed is required"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                if 'recieverName' in d.keys():
                    sentCard.recieverName = d['recieverName']
                if ("cardPic" in d.keys()):
                    if not d['cardPic']:
                        return Response(
                            {"data": "Please upload you cardPic", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if (isinstance(d['cardPic'], str)):
                        return Response(
                            {"data": "Please upload you cardPic, it cannot be string", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if (isinstance(d['cardPic'], dict)):
                        if (isinstance(d['cardPic'], dict)):
                            if ("fileName" in d["cardPic"].keys()):
                                url = d['cardPic']["filePath"]
                                url = url.split(",")
                                filedata = base64.b64decode(url[1])
                                name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + d['cardPic'][
                                    'fileName']
                                filename = str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + name
                                with open(filename, 'wb') as f:
                                    f.write(filedata)
                                    f.close()

                                    if (sentCard.cardPic):
                                        if os.path.exists(
                                                str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + sentCard.cardPic):
                                            os.remove(str(settings.BASE_DIR) + r"\my_Gift/uploads\\" + sentCard.cardPic)

                                    sentCard.cardPic = name

                sentCard.save()
                notification_to = getReceive_by_Phonenumber(d['receiverPhone'])
                cart_id = generateCartId(card, user.Id)
                if (d['isClaimed'] == True and notification_to is not None):
                    trans = Transactions(
                        cart_id=cart_id,
                        amount=card.amount,
                        currency="SAR",
                        status_code=0,
                        status_message="Paid",
                        payment_type="Gift_Card",
                        sent_by=user,
                        sent_to=notification_to.Id,
                        customer_name=notification_to.UserName,
                        customer_email=notification_to.Email,

                        card_id=card,

                        creation_time=datetime.datetime.now()
                    )
                    trans.save()

                if (notification_to is None):
                    pass
                else:
                    notification = Notifications(
                        notification_by=user,
                        notification_to=str(notification_to.Id),
                        description="You update your sended card to" + notification_to.UserName
                    )
                    notification.save()

                data = model_to_dict(sentCard)
                data['card'] = model_to_dict(sentCard.card)
                data['senderId'] = (UserSerializer(sentCard.senderId)).data
                if (sentCard.senderId.profilePic):
                    data['senderId']['profilePic'] = str(IMG_URL) + "/my_Gift/uploads/" + str(
                        sentCard.senderId.profilePic)
                if (sentCard.cardPic):
                    pp = str(IMG_URL) + "/my_Gift/uploads/" + str(name)
                    data['cardPic'] = pp

                return Response({"data": data,"cart_Id":cart_id, "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            # print(ex)
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})


class ReceiveCardsByPhoneNumberUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            d = request.data
            data = []
            if ('phoneNumber' in d.keys()):
                phoneNumber = d['phoneNumber']
                if not d['phoneNumber']:
                    return Response(
                        {
                            'data': 'phoneNumber cannot be empty',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'data': 'phoneNumber is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            cards = getReceiveCard_by_Phonenumber(phoneNumber)
            if (cards is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                for card in cards:
                    cardData = model_to_dict(card)

                    if (cardData['cardPic']):
                        cardData['cardPic'] = img_url(cardData['cardPic'])

                    cardData['card'] = model_to_dict(card.card)
                    cardData['senderId'] = UserSerializer(card.senderId).data
                    if (card.senderId.profilePic):
                        cardData['senderId']['profilePic'] = img_url_profile(card.senderId.profilePic)
                    data.append(cardData)

                return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})

class ReceiveCardsByUserIdUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        #  pk = str(pk).replace('"', '')
        # cards = Cards.objects.get(pk=pk)
        try:

            data = []
            cards =getSendCard_by_UserId(pk)
            for card in cards:
                cardData = model_to_dict(card)
                if (card.cardPic):
                    cardData['cardPic'] = img_url(card.cardPic)
                cardData['card'] = model_to_dict(card.card)
                cardData['senderId'] = UserSerializer(card.senderId).data
                if (card.senderId.profilePic):
                    cardData['cardPic'] = img_url(card.senderId.profilePic)

                data.append(cardData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllClamedCardsUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:

            data = []
            cards =getAllClamiedSendCard()
            if (cards is None):
                return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            for card in cards:
                cardData = model_to_dict(card)
                cardData['card'] = model_to_dict(card.card)

                if(card.cardPic):
                    cardData['cardPic']  = img_url(card.cardPic)
                cardData['senderId'] = UserSerializer(card.senderId).data
                if (card.senderId.profilePic):
                    cardData['senderId']['profilePic'] =img_url_profile(card.senderId.profilePic)
                data.append(cardData)



            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})


class ClamedCardsByUserIdUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        #  pk = str(pk).replace('"', '')
        # cards = Cards.objects.get(pk=pk)
        try:

            data = []
            cards =Clamied_Card_by_UserId(pk)
            for card in cards:
                cardData = model_to_dict(card)
                if (cardData['cardPic']):
                    cardData['cardPic'] = img_url(cardData['cardPic'])
                cardData['card'] = model_to_dict(card.card)
                cardData['senderId'] = UserSerializer(card.senderId).data
                if (card.senderId.profilePic):
                    cardData['senderId']['profilePic'] =img_url_profile(card.senderId.profilePic)
                data.append(cardData)

            return Response({"data": data, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TrueClamiedCardsUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:

            dic = request.data
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

            cards =getReceiveCard_by_Id(dic['Id'])
            if ('isClaimed' in dic.keys()):
                isClaimed = ['isClaimed']
            else:
                return Response(
                    {
                        'data': 'isClaimed is required',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


            if (cards is None):
                return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:

                isClaimed=dic['isClaimed']
                if (dic['isClaimed'] == True):
                    cards.isClaimed = isClaimed

                    cards.save()
                    user = getUser_by_Ph(cards.receiverPhone) #getUser_by_Id(cards.senderId)
                    if (user is None):
                        return Response({"data": "user doesn't exists on Card receiverPhone", "status": status.HTTP_404_NOT_FOUND},
                                        status=status.HTTP_404_NOT_FOUND)

                    card = cards.card #getCard_by_Id(cards.card)
                    if (card is None):
                        return Response({"data": "card doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                        status=status.HTTP_404_NOT_FOUND)

                    cart_id = generateCartId(card, user)
                    notification = Notifications(
                        notification_by=user,
                        notification_to=str(user.Id),
                        description= "You have claimed the card successfully"
                    )
                    notification.save()
                    trans = Transactions(
                        cart_id=cart_id,
                        amount=card.amount,
                        currency="SAR",
                        status_code=0,
                        status_message="Paid",
                        payment_type="Gift_Card",
                        sent_by=user,
                        sent_to=cards.senderId.Id,
                        customer_name=cards.senderId.UserName,
                        customer_email=cards.senderId.Email,
                        description="",
                        card_id=card,

                        creation_time=datetime.datetime.now()
                    )
                    trans.save()
                    data = model_to_dict(cards)

                    if (cards.cardPic):
                        data['cardPic'] = img_url(cards.cardPic)
                    data['senderId'] = UserSerializer(cards.senderId).data
                    if (cards.senderId.profilePic):
                        data['senderId']['profilePic'] = img_url_profile(cards.senderId.profilePic)

            return Response({"data": data,"cart_Id":cart_id, "status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_403_FORBIDDEN})