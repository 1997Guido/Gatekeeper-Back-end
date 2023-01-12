from ..models import UserProfile
from ..models import Event
from cryptography.fernet import Fernet
import json

def QrCodeVerificator(user, request):
    uid = UserProfile.objects.get(pk=user["pk"]).QrUid
    user = (
    UserProfile.objects.filter(pk=request.user.pk)
    .values(
        "first_name",
        "last_name",
        "gender",
        "date_of_birth"
        )
        .first()
    )
    
    

    qrdata = json.loads(request.body.decode("utf-8"))["encryptedqrdata"]
    
    #eventpk = json.loads(request.body.decode("utf-8"))["event"]
    
    #event = Event.objects.get(pk=eventpk)
    
    #guestlist = (list(event.EventInvitedGuests.values()))
    
    
    QrData = str(qrdata).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    QrDataDecrypted = f.decrypt(QrData)
    
    QrDataDecrypted = QrDataDecrypted.decode('utf-8')
    
    if QrDataDecrypted == uid:
        check = "True"
        notjsondata = {
        "userdata": user,
        "check": check
        }
        
        jsondata = json.dumps(notjsondata, default=str)
        
        return (jsondata)
    else:
        return (False)