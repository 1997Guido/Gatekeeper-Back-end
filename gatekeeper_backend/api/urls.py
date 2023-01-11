from django.urls import path
from .views import UserProfileView
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi
from .views import AuthCheckApi
from .views import QrCodeVerificatorApi
from .views import EventCreationApi
from .views import EventViewApi
from .views import EventViewApiPersonal
from .views import EventEditApi
from .views import UsernameViewApi
from .views import EventDeleteApi
from .views import EventInviteApi
from .views import ViewSingleEvent
urlpatterns = [
    path('profiles', UserProfileView.as_view()),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
    path('authcheck', AuthCheckApi),
    path('qrcodeverificatorapi', QrCodeVerificatorApi),
    path('eventcreationapi', EventCreationApi.as_view()),
    path('eventviewapi', EventViewApi.as_view()),
    path('eventviewapipersonal', EventViewApiPersonal.as_view()),
    path('eventeditapi', EventEditApi),
    path('usernamelistviewapi', UsernameViewApi.as_view()),
    path('eventdeleteapi', EventDeleteApi),
    path('eventinviteapi', EventInviteApi),
    path('viewsingleevent', ViewSingleEvent.as_view()),
    
]
