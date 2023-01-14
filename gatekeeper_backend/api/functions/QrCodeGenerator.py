from ..models import UserProfile
import random, string
import qrcode
from cryptography.fernet import Fernet

def QrCodeGenerator(user):
    length = 16
    uid = UserProfile.objects.get(pk=user["pk"]).QrUid
        
    if uid == '0':
        while True:
            uid = ''.join(random.choices(string.ascii_uppercase, k=length))
            if UserProfile.objects.filter(QrUid=uid).exists():
                continue
            else:
                UserProfile.objects.filter(pk=user["pk"]).update(QrUid=uid)
                break

    
    id = UserProfile.objects.get(pk=user["pk"]).QrUid
    
    UserData = str(id).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    UserDataEncrypted = f.encrypt(UserData)
    
    #qr_data = UserDataEncrypted

    #qr_img = qrcode.make(qr_data)

    #qr_img.save("qrdir/qrTest.png")
    
    return (UserDataEncrypted)