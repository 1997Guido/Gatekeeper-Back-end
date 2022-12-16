from ..models import UserProfile
from cryptography.fernet import Fernet
import difflib

def QrCodeVerificator(user):
    uid = UserProfile.objects.get(pk=user["pk"]).QrUid

    id = "gAAAAABjnGow0H7M7giwA0nZ49dcLfXYLaipVzDUyqn69ArIUKzkgG9nV76A52OQQX0ym5I4Z83AUUsce-w1k4Rs4WJ2mYhpcA=="
    
    QrData = str(id).encode('utf-8')
    key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="
    f = Fernet(key)
    
    QrDataDecrypted = f.decrypt(QrData)
    
    QrDataDecrypted = QrDataDecrypted.decode('utf-8')
    
    if QrDataDecrypted == uid:
        return True
    else:
        return False
    
    #return('\n'.join(difflib.ndiff([QrDataDecrypted], [uid])))
    
    #return (QrDataDecrypted, uid)