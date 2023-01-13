from ..models import UserProfile
from ..models import Event
from cryptography.fernet import Fernet
import json

def QrCodeVerificator(request):
    qrdata = json.loads(request.body.decode("utf-8"))["encryptedqrdata"]
    
    eventpk = json.loads(request.body.decode("utf-8"))["event"]
    
    event = Event.objects.get(pk=eventpk)
    
    guestlist = (list(event.EventInvitedGuests.values()))
    
    
    QrData = str(qrdata).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    QrDataDecrypted = f.decrypt(QrData)
    
    QrDataDecrypted = QrDataDecrypted.decode('utf-8')
    
    user = UserProfile.objects.get(QrUid=QrDataDecrypted)
    #userobject = (list(user.values()))
    
    if QrDataDecrypted == user.QrUid:
        check = "True"
        notjsondata = {
        #"user": userobject,
        "userdata": {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        },
        "guestlist": guestlist,
        "check": check
        }
        
    jsondata = json.dumps(notjsondata, default=str)
    
    return (jsondata)