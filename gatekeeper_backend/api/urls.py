from django.urls import path
from .views import UserProfileView
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi
from .views import AuthCheckApi
from .views import QrCodeVerificatorApi
from .views import EventViewApi
from .views import EventCreationApi


urlpatterns = [
    path('profiles', UserProfileView.as_view()),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
    path('authcheck', AuthCheckApi),
    path('qrcodeverificatorapi', QrCodeVerificatorApi),
    path('eventviewapi', EventViewApi),
    path('eventcreationapi', EventCreationApi),
]
