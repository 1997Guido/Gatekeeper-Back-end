from ..models import UserProfile

#This is the profile view, it returns the profile of the user who is logged in
#request.user is the logged in user.
def ProfileLogic(request):
    user = (
        UserProfile.objects.filter(pk=request.user.pk)
        .values(
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "gender",
        )
        .first()
    )
    return(user)
