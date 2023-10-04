import json

import cryptography
from api.models import Event, User
from cryptography.fernet import Fernet

# This file contains the code for generating and verifying the qr codes


class QRCodeHandler:
    def __init__(self, request):
        self.request = request
        self.key = "rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="

    # Helper functions for encrypting and decrypting the qr code
    def _encrypt(self, data: bytes) -> bytes:
        f = Fernet(self.key)
        return f.encrypt(data)

    def _decrypt(self, data: bytes) -> bytes:
        f = Fernet(self.key)
        try:
            return f.decrypt(data)
        except cryptography.fernet.InvalidToken:
            raise ValueError("Invalid QR Code - Not a Fernet encrypted token")

    def generate(self):
        user = User.objects.get(pk=self.request.user.pk)
        encrypted_qr_uid = self._encrypt(str(user.QrUid).encode("utf-8"))
        return encrypted_qr_uid

    def verify(self):
        request_data = json.loads(self.request.body.decode("utf-8"))
        qr_data = request_data["encryptedqrdata"]
        event_pk = request_data["event"]

        event = Event.objects.get(pk=event_pk)

        try:
            qr_data_decrypted = self._decrypt(qr_data.encode("utf-8")).decode("utf-8")
        except ValueError as e:
            print(str(e))
            return (None, None, False)  # Indicate an error

        user = User.objects.get(QrUid=qr_data_decrypted)

        if qr_data_decrypted == user.QrUid:
            if event.is_invited(user):
                return (user, True)
            else:
                return (user, False)
