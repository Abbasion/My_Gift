
from django.urls import path

from my_Gift.Models.AddData.AddData import addData
from my_Gift.Models.AdminWallet.adminWallet import AdminWalletListUpdateAPIView
from my_Gift.Models.Cards.cards import CardsListUpdateAPIView
from my_Gift.Models.ContactUs.contactUs import ContactUsListUpdate
from my_Gift.Models.Nifications.notifications import NotificationListUpdateAPIView
from my_Gift.Models.PendingProfile.pendingProfile import PendingProfileAPIView, GetAllPartnerAPIView, \
    PendingProfileBYUserIdUpdateToUserAPIView
from my_Gift.Models.ResetPassword.resetPassword import Forget_password, resendActivationLink, Reset
from my_Gift.Models.SendReceiveCards.sendReceiveCards import SendReceiveCardsUpdateAPIView, \
    ReceiveCardsByUserIdUpdateAPIView, AllClamedCardsUpdateAPIView, ReceiveCardsByPhoneNumberUpdateAPIView, \
    ClamedCardsByUserIdUpdateAPIView, TrueClamiedCardsUpdateAPIView
from my_Gift.Models.Transactions.transactions import TransactionsListUpdateAPIView, TransactionsByUserIdUpdateAPIView, \
    AdminTransactionsListUpdateAPIView, AdminCardTransactionsListUpdateAPIView, UserTransactionsListUpdateAPIView, \
    UserAllTransactionsListUpdateAPIView, PartnerTransactionsListUpdateAPIView
from my_Gift.Models.Users.Login import CreateUserAPIView, Login, UserRetrieveAPIView, AdminRetrieveUpdateAPIView, \
    TokenVerify
from my_Gift.Models.Wallet.wallet import WalletsByUserIdUpdateAPIView, WalletListUpdateAPIView
from my_Gift.Models.Withdrawal.withdrawal import WidthDrawalAPIView

urlpatterns = [
    path('migrate/', addData),
    path('verify/', TokenVerify.as_view(), name='token_verify'),
    path('user/registration/', CreateUserAPIView.as_view()),
    path('login/', Login),
    path('user/all/', UserRetrieveAPIView.as_view()),
    path('user/all/admin/', AdminRetrieveUpdateAPIView.as_view()),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view()),
    path('user/email/', UserRetrieveAPIView.as_view()),
    path('user/phone/', UserRetrieveAPIView.as_view()),
    path('partner/request/create/', PendingProfileAPIView.as_view()),
    path('pending/profile/all/', PendingProfileAPIView.as_view()),
    path('partner/all/', GetAllPartnerAPIView.as_view()),
    path('partner/user/update/status/', PendingProfileBYUserIdUpdateToUserAPIView.as_view()),
    path('wallet/byuser/<int:pk>/', WalletsByUserIdUpdateAPIView.as_view()),
    path('wallet/user/update/', WalletsByUserIdUpdateAPIView.as_view()),
    path('wallet/<int:pk>/', WalletListUpdateAPIView.as_view()),
    path('wallet/', WalletListUpdateAPIView.as_view()),
    path('admin/wallet/', AdminWalletListUpdateAPIView.as_view()),
    path('admin/wallet/<int:pk>/', AdminWalletListUpdateAPIView.as_view()),
    path('card/create/', CardsListUpdateAPIView.as_view()),
    path('card/<int:pk>/', CardsListUpdateAPIView.as_view()),
    path('card/all/', CardsListUpdateAPIView.as_view()),
    path('card/send/', SendReceiveCardsUpdateAPIView.as_view()),
    path('card/send/<int:pk>/', SendReceiveCardsUpdateAPIView.as_view()),
    path('card/receivebyuser/<int:pk>/', ReceiveCardsByUserIdUpdateAPIView.as_view()),
    path('all/send/clamied/card/', AllClamedCardsUpdateAPIView.as_view()),
    path('card/receive/', ReceiveCardsByPhoneNumberUpdateAPIView.as_view()),
    path('card/claimedbyuser/<int:pk>/', ClamedCardsByUserIdUpdateAPIView.as_view()),
    path('card/claimed/', TrueClamiedCardsUpdateAPIView.as_view()),
    path('notifications/<int:pk>/', NotificationListUpdateAPIView.as_view()),
    path('notifications/', NotificationListUpdateAPIView.as_view()),
    path('notifications/byuser/<int:pk>/', NotificationListUpdateAPIView.as_view()),
    path('withdrawal/', WidthDrawalAPIView.as_view()),
    path('transactions/<int:pk>/', TransactionsListUpdateAPIView.as_view()),
    path('transactions/update/', TransactionsListUpdateAPIView.as_view()),
    path('transactions/all/', TransactionsListUpdateAPIView.as_view()),
    path('transactions/byuserid/<int:pk>/', TransactionsByUserIdUpdateAPIView.as_view()),
    path('password/forget/', Forget_password.as_view()),
    path('resend/email/<str:uid>/', resendActivationLink),
    path('reset/<uidb64>/<token>/', Reset, name="reset_pass"),
    path('contact/us/', ContactUsListUpdate.as_view()),
    path('contact/us/<int:pk>/', ContactUsListUpdate.as_view()),
    path('admin/transactions/', AdminTransactionsListUpdateAPIView.as_view()),
    path('admin/card/transactions/', AdminCardTransactionsListUpdateAPIView.as_view()),
    path('user/transactions/', UserTransactionsListUpdateAPIView.as_view()),
    path('user/transactions/all/', UserAllTransactionsListUpdateAPIView.as_view()),
    path('partner/transactions/', PartnerTransactionsListUpdateAPIView.as_view()),

]
