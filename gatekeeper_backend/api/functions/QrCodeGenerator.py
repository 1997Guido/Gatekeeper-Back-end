from ..models import QrCode
import random, string


def generate_unique_id():
    length = 8
    
    while True:
        uid = ''.join(random.choices(string.ascii_uppercase, k=length))
        if QrCode.objects.filter(QrUid=uid).count() == 0:
            break
        
    return uid


def QrCodeGenerator():
    uuid = generate_unique_id()
    return (uuid)
