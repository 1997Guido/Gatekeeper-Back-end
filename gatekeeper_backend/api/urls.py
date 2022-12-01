from django.urls import path, include
from .views import UserProfileView
from .views import RegisterApi
from .views import QrCodeGeneratorApi
from .views import QrCodeScannerApi
from .views import ProfileApi





urlpatterns = [
    path('home', UserProfileView.as_view()),
    path('registerapi', RegisterApi),
    path('qrcodegeneratorapi', QrCodeGeneratorApi),
    path('qrcodescannerapi', QrCodeScannerApi),
    path('profileapi', ProfileApi),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
