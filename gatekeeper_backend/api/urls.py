from django.urls import path, include
from . import views

# These are the paths which the frontend calls
# They are called by the frontend using the axios library

urlpatterns = [
    path('profiles', views.UserProfileView.as_view()),
    path('qrcodegeneratorapi', views.QrCodeGeneratorApi),
    path('profileapi', views.UserProfileView.as_view()),
    path('profiledeleteapi', views.ProfileDeleteApi.as_view()),
    path('authcheck', views.AuthCheckApi),
    path('qrcodeverificatorapi', views.QrCodeVerificatorApi),
    path('eventcreationapi', views.EventCreationApi.as_view()),
    path('eventviewapi', views.EventViewApi.as_view()),
    path('eventviewapipersonal', views.EventViewApiPersonal.as_view()),
    path('eventeditapi', views.EventEditApi),
    path('usernamelistviewapi', views.UsernameViewApi.as_view()),
    path('eventdeleteapi', views.EventDeleteApi),
    path('eventinviteapi', views.EventInviteApi),
    path('viewsingleevent', views.ViewSingleEvent.as_view()),
    path('getinvitedusers', views.getInvitedUsers),
    path('usernameviewapi', views.UsernameViewApi.as_view()),
    path('profileeditapi', views.ProfileEditApi.as_view()),
    path('imageview', views.ImageViewApi.as_view()),
    path('setprofileimage', views.SetProfileImage),
]
