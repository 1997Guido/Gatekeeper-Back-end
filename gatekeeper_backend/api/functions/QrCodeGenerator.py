from ..models import UserProfile
import random, string, base64, os
import qrcode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_unique_id():
    length = 8
    
    while True:
        uid = ''.join(random.choices(string.ascii_uppercase, k=length))
        if UserProfile.objects.filter(QrUid=uid).count() == 0:
            break
        
    return uid

def QrCodeGenerator(user):
    UserProfile.objects.filter(pk=user["pk"]).update(QrUid=generate_unique_id())
    ##user["QrUid"] = generate_unique_id()
    
    ##UserDataJson = json.dumps(user, ensure_ascii=False)

    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    temp = "\n[ " #For testing purposes
    temp2 = " ]\n" #For testing purposes
    
    #UserDataEncrypted = f.encrypt(user.encode())

    qr_data = user

    qr_img = qrcode.make(qr_data)

    qr_img.save("qrdir/qrTest.png")
    
    return (user)