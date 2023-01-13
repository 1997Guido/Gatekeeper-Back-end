from ..models import UserProfile
from ..models import Event
from cryptography.fernet import Fernet
import json

def QrCodeVerificator(request):
    
    eventpk = json.loads(request.body.decode("utf-8"))["event"]
    
    event = Event.objects.filter(pk=eventpk)
    
    guestlist = (list(event.EventInvitedGuests.values("pk")))
    

    qrdata = json.loads(request.body.decode("utf-8"))["encryptedqrdata"]
    
    QrData = str(qrdata).encode('utf-8')
        
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
        
    QrDataDecrypted = f.decrypt(QrData)
    QrDataDecrypted = QrDataDecrypted.decode('utf-8')
    
    user = UserProfile.objects.filter(QrUid=QrDataDecrypted)
    
           

        
    check = "True"
    notjsondata = {
    "userdata": user,
    "check": check,
    }
                        
    jsondata = json.dumps(notjsondata, default=str)
    
pkcheck = False
for value in guestlist:
    if value["pk"] == user.pk:
        pkcheck = True
        break
    else:
        pkcheck = False
            
            
if pkcheck == True:                
    return (jsondata)
else:
    return ("False")
