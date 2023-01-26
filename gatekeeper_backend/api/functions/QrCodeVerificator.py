from ..models import UserProfile
from ..models import Event
from ..models import Image
from cryptography.fernet import Fernet
import json
from binascii import Error
from cryptography import *
import cryptography

# QrCodeVerificator takes the request from the frontend and decrypts the encrypted qr data.
# It then checks if the decrypted qr data matches the qr data of the user in the database.
# If the qr data matches the user in the database, it checks if the user is invited to the event.
# If the user is invited to the event, it returns the user data to the frontend.
# If the user is not invited to the event, it returns a check value of false.


def QrCodeVerificator(request):
    try:
        qrdata = json.loads(request.body.decode("utf-8"))["encryptedqrdata"]
        
        eventpk = json.loads(request.body.decode("utf-8"))["event"]
        
        event = Event.objects.get(pk=eventpk)
        
        userlist = (list(event.EventInvitedGuests.values()))

        guestlist = []

        # This for loop is used to create a list of the user ids of the invited guests.
        for value in userlist:
            guestlist.append(value["id"])
        
        # Here the qr data is decrypted.
        QrData = str(qrdata).encode('utf-8')
        key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
        f = Fernet(key)
        
        QrDataDecrypted = f.decrypt(QrData)
        
        QrDataDecrypted = QrDataDecrypted.decode('utf-8')
        
        # This gets the user that is linked to the scanned qr code from the database.
        user = UserProfile.objects.get(QrUid=QrDataDecrypted)

        guestcheck = False

        # Get the profile picture of the user.
        try:
            image = Image.objects.get(pk=user.ProfilePicture_id)
            imageurl = image.Image.url
        except:
            imageurl = None


        # This if statement checks if the user is invited to the event.
        if user.pk in guestlist:
            guestcheck = True

        if QrDataDecrypted == user.QrUid:
            # If the user is invited to the event, it returns the user data, a check value of true and an invited value of true to the frontend.
            if guestcheck == True:
                check = "true"
                notjsondata = {
                "userdata": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth": user.date_of_birth,
                "gender": user.gender,
                "imageurl": imageurl,
                },
                "invited": "true",
                "check": check,
                }

            # If the user is not invited to the event, it returns a invited value of false.
            else:
                check = "true"
                notjsondata = {
                "check": check,
                "invited": "false"
                }
        # If the qr data does not match the user in the database, it returns a check value of false.
        else:
            check = "false"
            notjsondata = {
            "check": check,
            "user not found": "User not Found" 
            }
            
        # Convert the data to json.
        jsondata = json.dumps(notjsondata, default=str)
        
        return (jsondata)
        
    except:
        check = "false"
        notjsondata2 = {
        "check": check,
        "Fernet error": "Fernet error" 
        }
                
        jsondata2 = json.dumps(notjsondata2, default=str)
            
        return (jsondata2)