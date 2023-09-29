import json

import cryptography
from cryptography.fernet import Fernet

from ..models import Event, Image, User

#############################################################################
#                                                                           #
#   This file contains the code for generating and verifying the qr codes   #
#                                                                           #
#   Created by Mike C. Vermeer                                              #
#                                                                           #
#############################################################################


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
        if not user.QrUid:
            raise ValueError("User does not have a QrUid")

        encrypted_qr_uid = self._encrypt(str(user.QrUid).encode("utf-8"))
        return encrypted_qr_uid

    def verify(self):
        request_data = json.loads(self.request.body.decode("utf-8"))
        qr_data = request_data["encryptedqrdata"]
        event_pk = request_data["event"]

        event = Event.objects.get(pk=event_pk)
        userlist = event.get_guests
        guestlist = [value["id"] for value in userlist]

        try:
            qr_data_decrypted = self._decrypt(qr_data.encode("utf-8")).decode("utf-8")
        except ValueError as e:
            print(str(e))
            return (None, None, False)  # Indicate an error

        user = User.objects.get(QrUid=qr_data_decrypted)

        is_guest = user.pk in guestlist

        imageurl = None
        if user.ProfilePicture_id:
            try:
                image = Image.objects.get(pk=user.ProfilePicture_id)
                imageurl = image.Image.url
            except Image.DoesNotExist:
                pass

        if qr_data_decrypted == user.QrUid:
            if is_guest:
                return (user, imageurl, True)
            else:
                return (user, imageurl, False)
