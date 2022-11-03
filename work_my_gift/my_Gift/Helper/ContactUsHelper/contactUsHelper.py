from my_Gift_app.Models.ContactUs.contactUs import ContactUs


def contact_us_by_Id(Id):
    try:
        cons = ContactUs.objects.get(pk=Id,isDeleted=False)
        return cons
    except:
        return None

def get_all_contact():
    try:
        cons = ContactUs.objects.filter(isDeleted=False).order_by("-Id")
        return cons
    except:
        return None