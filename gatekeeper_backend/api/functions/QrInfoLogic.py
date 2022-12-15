from ..models import UserProfile
from .QrCodeGenerator import QrCodeGenerator
#This is the profile view, it returns the profile of the user who is logged in
#request.user is the logged in user.
def QrInfoLogic(request):
    user = (
        UserProfile.objects.filter(pk=request.user.pk)
        .values(
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
            "QrUid",
        )
        .first()
    )

    return(QrCodeGenerator(user))
