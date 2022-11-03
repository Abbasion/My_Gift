from django.db.models import Q

from my_Gift_app.Models.Transactions.transactions import Transactions


def get_transaction_by_Id(Id):
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").get(isDeleted=False,pk=Id)
        return trans
    except:
        return None

def get_transaction_by_User_Id(sent_by):
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,sent_to=sent_by ) | Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,sent_by=sent_by )
        return trans
    except:
        return None

def getAllTransactions():
    try:
        list = Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False).order_by("-Id")
        return list
    except Exception as ex:
        return None

def get_Admin_Transactions_Receive():
    try:
        # store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,sent_by__payment_type='Admin_receive').order_by("-Id")
        store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Admin_receive').order_by("-Id")
        return store
    except:
        return None

def get_Admin_Transactions_send():
    try:
        store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Admin_send').order_by("-Id")
        return store
    except:
        return None
def get_Admin_Transactions_card():
    try:
        store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Admin_card').order_by("-Id")
        return store
    except:
        return None

def get_all_Admin_Transactions():
    try:
        store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Admin_send')|Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Admin_receive')|Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Admin_card').order_by("-Id").order_by("-Id")
        return store
    except:
        return None


def get_User_Transactions_Card():
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Gift_Card').order_by("-Id")
        return trans
    except:
        return None

def get_User_Wallet_Transactions():
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='user_wallet').order_by("-Id")
        return trans
    except:
        return None
def get_User_withdraw_Transactions():
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='user_withdrawal').order_by("-Id")
        return trans
    except:
        return None

def get_all_User_Transactions():
    try:
        store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='user_withdrawal')|Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='user_wallet')|Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='Gift_Card').order_by("-Id").order_by("-Id")
        return store
    except:
        return None




def get_Partner_Wallet_Transactions():
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='partner_wallet').order_by("-Id")
        return trans
    except:
        return None
def get_partner_withdraw_Transactions():
    try:
        trans=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='partner_withdrawal').order_by("-Id")
        return trans
    except:
        return None

def get_all_Partner_Transactions():
    try:
        store=Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='partner_withdrawal')|Transactions.objects.select_related("sent_by","card_id").filter(isDeleted=False,payment_type='partner_wallet').order_by("-Id").order_by("-Id")
        return store
    except:
        return None