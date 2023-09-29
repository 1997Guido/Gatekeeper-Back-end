from django.urls import path

from . import views

# These are the paths which the frontend calls
# They are called by the frontend using the axios library

urlpatterns = [
    # Events
    path("event/<int:pk>/", views.EventDetailView.as_view()),
    path("eventslist/", views.EventListView.as_view()),
    path("eventslist/<int:pk>/", views.EventListView.as_view()),
    path("eventinvite/<int:pk>/", views.EventInviteView.as_view()),
    path("eventuninvite/<int:pk>/", views.EventUninviteView.as_view()),
    path("eventcreate", views.EventCreateView.as_view()),
    path("eventupdate/<int:pk>/", views.EventUpdateView.as_view()),
    path("eventdelete/<int:pk>/", views.EventDeleteView.as_view()),
    # User
    path("authcheck", views.AuthCheckView),
    path("users", views.UserView.as_view()),
    path("username", views.UsernameViewApi.as_view()),
    path("userupdate", views.UserUpdateView.as_view()),
    path("userdelete", views.UserDeleteView.as_view()),
    # QR
    path("qrcodegeneratorapi", views.QrCodeGeneratorApi),
    path("qrcodeverificatorapi", views.QrCodeVerificatorApi),
    # Images
    path("image", views.ImageViewApi.as_view()),
    path("image/<int:pk>/", views.ImageViewApi.as_view()),
    path("profilepicture", views.ProfilePictureView.as_view()),
    path("profilepicture/<int:pk>/", views.ProfilePictureView.as_view()),
]
