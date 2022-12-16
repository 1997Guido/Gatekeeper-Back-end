from ..models import UserProfile
from cryptography.fernet import Fernet
import json

def QrCodeVerificator(user, request):
    uid = UserProfile.objects.get(pk=user["pk"]).QrUid

    qrdata = request.body.get("encryptedqrdata").decode("utf-8")

    
    
    QrData = str(qrdata).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    QrDataDecrypted = f.decrypt(QrData)
    
    QrDataDecrypted = QrDataDecrypted.decode('utf-8')
    
    if QrDataDecrypted == uid:
        return (True, " ", uid)
    else:
        return (False, "", uid)
    
    #return (QrDataDecrypted, uid)