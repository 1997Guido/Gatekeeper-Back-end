from django.urls import path
from .views import UserProfileView
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi





urlpatterns = [
    path('home', UserProfileView.as_view()),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
]
