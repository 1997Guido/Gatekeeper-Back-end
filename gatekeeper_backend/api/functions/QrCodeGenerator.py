from ..models import QrCode
from ..models import Users
import json
import random, string, base64, os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_unique_id():
    length = 8
    
    while True:
        uid = ''.join(random.choices(string.ascii_uppercase, k=length))
        if QrCode.objects.filter(QrUid=uid).count() == 0:
            break
        
    return uid

def QrCodeGenerator():
    UserData = {
        "first_name" : "Mike",
        "last_name" : "Vermeer",
        "age" : "20",
        "gender" : "Male",
        "admin" : "Yes",
        "uid" : ""
    }
    
    UserData["uid"] = generate_unique_id()
    
    UserDataJson = json.dumps(UserData, ensure_ascii=False)

    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    temp = "\n " #For testing purposes
    
    UserDataEncrypted = f.encrypt(UserDataJson.encode())
    
    return (UserDataJson, temp, UserDataEncrypted)