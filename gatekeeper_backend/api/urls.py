from django.urls import path
from .views import UsersView
from .views import RegisterApi
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi





urlpatterns = [
    path('home', UsersView.as_view()),
    path('registerapi', RegisterApi),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
]
