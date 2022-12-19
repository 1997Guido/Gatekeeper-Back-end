from django.urls import path
from .views import UserProfileView
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi
from .views import AuthCheckApi
from .views import QrCodeVerificatorApi




urlpatterns = [
    path('home', UserProfileView.as_view()),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
    path('authcheck', AuthCheckApi),
    path('qrcodeverificatorapi', QrCodeVerificatorApi),
]
