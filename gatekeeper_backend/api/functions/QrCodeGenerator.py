from ..models import UserProfile
import random, string, base64, os, json
import qrcode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_unique_id():
    length = 12
    
    while True:
        uid = ''.join(random.choices(string.ascii_uppercase, k=length))
        if UserProfile.objects.filter(QrUid=uid).count() == 0:
            break
        
    return uid

def QrCodeGenerator(user):
    UserProfile.objects.filter(pk=user["pk"]).update(QrUid=generate_unique_id())
    
    id = UserProfile.objects.get(pk=user["pk"]).QrUid
    
    UserData = str(id).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    UserDataEncrypted = f.encrypt(UserData)
    
    qr_data = UserDataEncrypted

    qr_img = qrcode.make(qr_data)

    qr_img.save("qrdir/qrTest.png")
    
    return (UserDataEncrypted)