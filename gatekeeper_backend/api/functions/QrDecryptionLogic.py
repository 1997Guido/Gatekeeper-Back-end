from ..models import UserProfile
from .QrCodeVerificator import QrCodeVerificator
#This is the profile view, it returns the profile of the user who is logged in
#request.user is the logged in user.

def QrDecryptionLogic(request):
    user = (
        UserProfile.objects.filter(pk=request.user.pk)
        .values(
            "pk",
            "QrUid",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
        )
        .first()
    )

    return(QrCodeVerificator(user))