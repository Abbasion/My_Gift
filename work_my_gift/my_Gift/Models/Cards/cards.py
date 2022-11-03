import datetime


from django.forms import model_to_dict

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_Gift.Helper.CardsHelper.cardsHelper import generateCartId, getallcards, getCard_by_Id
from my_Gift.Helper.imgurlhelper.urlhelper import img_url_profile
from my_Gift_app.Models.Cards.cards import Cards
from my_Gift_app.Models.Users.userSerializer import UserSerializer


class CardsListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            data = []
            card = getCard_by_Id(pk)
            if (card is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:

                data = model_to_dict(card)
                data['userId'] = UserSerializer(card.userId).data
                data['cartId'] = generateCartId(card, request.user.Id)
                if (card.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(card.userId.profilePic)

                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            cards = getallcards()
            for card in cards:
                cardData = model_to_dict(card)
                cardData['userId'] = UserSerializer(card.userId).data
                if (card.userId.profilePic):
                    cardData['userId']['profilePic'] = img_url_profile(card.userId.profilePic)
                else:
                    cardData['userId']['profilePic'] = ""
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

            isDeleted = ''
            if 'isDeleted' in d.keys():
                isDeleted = d['isDeleted']
            else:
                return Response(
                    {
                        'data': 'isDeleted is must be True or False',
                        'status': status.HTTP_400_BAD_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = request.user
            if (d['Id'] == 0 or d['Id'] == None):
                amount = ''
                if ('amount' in d.keys()):
                    amount = d['amount']
                    if not d['amount']:
                        return Response(
                            {
                                'data': 'amount cannot be empty and Zero(0)!',
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
                title=''
                if ('title' in d.keys()):
                    title = d['title']
                    if not d['title']:
                        return Response(
                            {
                                'data': 'title cannot be blank!',
                                'status': status.HTTP_400_BAD_REQUEST
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )

                else:
                    return Response(
                        {
                            'data': 'title is required',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                description=''
                if ('description' in d.keys()):
                    description = d['description']
                    if not d['description']:
                        return Response(
                            {
                                'data': 'description cannot be blank!',
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
                deduction = ''
                if ('deduction' in d.keys()):
                    deduction = d['deduction']
                    if not d['deduction']:
                        return Response(
                            {
                                'data': 'deduction cannot be blank and zero(0)!',
                                'status': status.HTTP_400_BAD_REQUEST
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                else:
                    return Response(
                        {
                            'data': 'deduction is required',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                color = ''
                if ('color' in d.keys()):
                    color = d['color']
                    if not d['color']:
                        return Response(
                            {
                                'data': 'color cannot be blank!',
                                'status': status.HTTP_400_BAD_REQUEST
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )

                else:
                    return Response(
                        {
                            'data': 'color is required',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                background_color = ''
                if ('background_color' in d.keys()):
                    background_color = d['background_color']
                    if not d['background_color']:
                        return Response(
                            {
                                'data': 'background_color cannot be blank!',
                                'status': status.HTTP_400_BAD_REQUEST
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )

                else:
                    return Response(
                        {
                            'data': 'background_color is required',
                            'status': status.HTTP_400_BAD_REQUEST
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                card = Cards(
                    userId=user,
                    amount=amount,  # d['amount'],
                    title=title,  # d['title'],
                    description=description,  # d['description'],
                    deduction=deduction,  # d['deduction'],
                    color=color,  # d['color'],
                    background_color=background_color,  # d['background_color'],
                    isDeleted=isDeleted,  # d['isDeleted'],
                    creation_time=datetime.datetime.now()


                )
                print(card.creation_time)
                cart_id = generateCartId(card, user.Id)
                card.save()

                data = model_to_dict(card)
                data['userId'] = (UserSerializer(card.userId)).data
                if (card.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(card.userId.profilePic)
                else:
                    data['userId']['profilePic'] = ""
                return Response({"data": data,"cart_id": cart_id,  "status": status.HTTP_201_CREATED},
                                status=status.HTTP_200_OK)



            else:
                card = Cards.objects.get(pk=d['Id'])
                card.userId = user
                card.isDeleted = isDeleted
                if 'title' in d.keys():
                    card.title = d['title']
                if 'amount' in d.keys():
                    card.amount = d['amount']
                if 'description' in d.keys():
                    card.description = d['description']
                if 'deduction' in d.keys():
                    card.deduction = d['deduction']
                if 'color' in d.keys():
                    card.color = d['color']
                if 'background_color' in d.keys():
                    card.background_color = d['background_color']
                card.creation_time = datetime.datetime.now()

                card.save()

                data = model_to_dict(card)
                data['userId'] = (UserSerializer(card.userId)).data
                if (card.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(card.userId.profilePic)
                else:
                    data['userId']['profilePic'] = ""
                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            # print(ex)
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)