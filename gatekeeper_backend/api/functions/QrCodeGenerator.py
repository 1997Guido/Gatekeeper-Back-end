from ..models import UserProfile
import random, string
import qrcode
from cryptography.fernet import Fernet


# QrCodeGenerator takes the request from the frontend and generates a qr code for the user.
# It then saves the qr code in the database and returns the qr code to the frontend.

def QrCodeGenerator(request):
    length = 16
    uid = UserProfile.objects.get(pk=request.user.pk).QrUid
        
    if uid == '0':
        while True:
            uid = ''.join(random.choices(string.ascii_uppercase, k=length))
            if UserProfile.objects.filter(QrUid=uid).exists():
                continue
            else:
                UserProfile.objects.filter(pk=request.user.pk).update(QrUid=uid)
                break

    
    id = UserProfile.objects.get(pk=request.user.pk).QrUid

    # The qr code is encrypted here.  
    UserData = str(id).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    UserDataEncrypted = f.encrypt(UserData)
    
    return (UserDataEncrypted)