from my_Gift_app.Models.AdminWallet.adminWallet import AdminWallet


def Admin_Wallet_by_Id():
    try:

        wallet = AdminWallet.objects.filter(isDeleted=False).first()
        return wallet
    except Exception as ex:
        return None

def get_admin_wallet_Id(Id):
    try:
        # card=Cards.objects.select_related("userId").filter(isDeleted=False)
        wallet = AdminWallet.objects.get(pk=Id,isDeleted=False)
        return wallet
    except:
        return None