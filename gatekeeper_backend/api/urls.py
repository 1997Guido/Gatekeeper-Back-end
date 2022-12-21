from django.urls import path
from .views import UserProfileView
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi
from .views import AuthCheckApi
from .views import QrCodeVerificatorApi
from .views import SingleEventApi
from .views import EventCreationApi
from .views import EventViewApi

urlpatterns = [
    path('profiles', UserProfileView.as_view()),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
    path('authcheck', AuthCheckApi),
    path('qrcodeverificatorapi', QrCodeVerificatorApi),
    path('singleeventapi', SingleEventApi),
    path('eventcreationapi', EventCreationApi.as_view()),
    path('eventviewapi', EventViewApi.as_view()),
]
