from ..models import UserProfile
from ..models import Event
from cryptography.fernet import Fernet
import json

# QrCodeVerificator takes the request from the frontend and decrypts the encrypted qr data.
# It then checks if the decrypted qr data matches the qr data of the user in the database.
# If the qr data matches the user in the database, it checks if the user is invited to the event.
# If the user is invited to the event, it returns the user data and the guestlist of the event.
# If the user is not invited to the event, it returns a check value of false.

def QrCodeVerificator(request):
    qrdata = json.loads(request.body.decode("utf-8"))["encryptedqrdata"]
    
    eventpk = json.loads(request.body.decode("utf-8"))["event"]
    
    event = Event.objects.get(pk=eventpk)
    
    userlist = (list(event.EventInvitedGuests.values()))

    guestlist = []

    # This for loop is used to create a list of the user ids of the invited guests.
    for value in userlist:
        guestlist.append(value["id"])
    
    QrData = str(qrdata).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    QrDataDecrypted = f.decrypt(QrData)
    
    QrDataDecrypted = QrDataDecrypted.decode('utf-8')
    
    user = UserProfile.objects.get(QrUid=QrDataDecrypted)

    guestcheck = False

    # This if statement checks if the user is invited to the event.
    if user.pk in guestlist:
        guestcheck = True

    if QrDataDecrypted == user.QrUid:
        if guestcheck == True:
            check = "true"
            notjsondata = {
            "userdata": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth,
            "gender": user.gender,
            },
            "guestlist": guestlist,
            "check": check,
            "userpk": user.pk,
            }
        else:
            check = "false"
            notjsondata = {
            "check": check
            }
    else:
        check = "false"
        notjsondata = {
        "check": check
        }
        
    jsondata = json.dumps(notjsondata, default=str)
    
    return (jsondata)