from ..models import UserProfile
import random, string
import qrcode
from cryptography.fernet import Fernet


# QrCodeGenerator takes the request from the frontend and generates a unique code for the user.
# It then saves the code in the database.
# This code is then encrypted and returned to the frontend.
# The frontend then converts the data into a QR code and displays it to the user.

def QrCodeGenerator(request):
    # Length must be the same as the length of the QrUid charfield in the database.
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

    # The qr code is encrypted here using Fernet.  
    UserData = str(id).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key) 
    UserDataEncrypted = f.encrypt(UserData)
    
    return (UserDataEncrypted)