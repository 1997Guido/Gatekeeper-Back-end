# Checks if the user is authenticated
def AuthCheck(request):
    if (request.user.is_authenticated):
        return("true")
    else:
        return("false")