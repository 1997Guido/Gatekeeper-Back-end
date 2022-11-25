from ..models import QrCode
from ..models import Users
import json
import random, string, base64

def generate_unique_id():
    length = 8
    
    while True:
        uid = ''.join(random.choices(string.ascii_uppercase, k=length))
        if QrCode.objects.filter(QrUid=uid).count() == 0:
            break
        
    return uid

def QrCodeGenerator(UserData):
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
    UserData_bytes = UserDataJson.encode('ascii')
    base64_bytes = base64.b64encode(UserData_bytes)
    base64_UserData = base64_bytes.decode('ascii')

    
    
    return (UserDataJson, base64_UserData)