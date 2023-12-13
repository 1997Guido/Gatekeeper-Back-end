import base64
from datetime import datetime, timedelta

import cryptography
from api.models import Event, User
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# This file contains the code for generating and verifying the qr codes


class ExceptionTokenExpired(Exception):
    pass


class ExceptionInvalidToken(Exception):
    pass


class QRCodeHandler:
    def __init__(self, request):
        self.request = request
        self.key = self._derive_key(request.user)

    def _derive_key(self, user):
        # Using Django's PBKDF2PasswordHasher
        hasher = PBKDF2PasswordHasher()
        # Derive a key from the user's unique attributes (Primary Key and Password)
        raw_key = hasher.encode(password=user.password, salt=str(user.id), iterations=50000)

        # Fernet keys should be 32 url-safe base64-encoded bytes.
        # So, we'll take the first 32 bytes of our derived key, and encode it to get a valid Fernet key
        key = base64.urlsafe_b64encode(raw_key.encode()[:32])
        return key

    def _get_token_age(self, token: bytes) -> timedelta:
        f = Fernet(self.key)
        timestamp = f.extract_timestamp(token)
        token_time = datetime.utcfromtimestamp(timestamp)
        current_time = datetime.utcnow()
        token_age = current_time - token_time
        return token_age

    # Helper functions for encrypting and decrypting the qr code
    def _encrypt(self, data: bytes) -> bytes:
        f = Fernet(self.key)
        return f.encrypt(data)

    def _decrypt(self, data: bytes) -> bytes:
        f = Fernet(self.key)
        try:
            return f.decrypt(data)
        except cryptography.fernet.InvalidToken:
            raise ExceptionInvalidToken("The token is invalid.")

    def generate(self):
        user = User.objects.get(pk=self.request.user.pk)
        encrypted_qr_uid = self._encrypt(str(user.QrUid).encode("utf-8"))
        # Append the user ID to the encrypted data
        qr_data = f"{user.id}:{encrypted_qr_uid.decode('utf-8')}"
        return qr_data

    def verify(self):
        event_pk = self.request.data["event"]
        qr_data = self.request.data["encryptedqrdata"]
        
        # Split the QR data to get the user ID and the encrypted data
        user_id_str, encrypted_qr_data = qr_data.split(':', 1)
        user_id = int(user_id_str)
        encrypted_qr_data = encrypted_qr_data.encode("utf-8")

        # Use the user ID to derive the key
        user = User.objects.get(pk=user_id)
        self.key = self._derive_key(user)
        
        try:
            qr_data_decrypted = self._decrypt(encrypted_qr_data).decode("utf-8")
            token_age = self._get_token_age(encrypted_qr_data)

            if token_age > timedelta(seconds=60):
                raise ExceptionTokenExpired("The token has been expired for more than 60 seconds.")

            user = User.objects.get(QrUid=qr_data_decrypted)

            event = Event.objects.get(pk=event_pk)
            if not event.is_invited(user):
                return (user, False)

            return (user, True)

        except ExceptionTokenExpired:
            raise
        except ExceptionInvalidToken:
            raise
        except Exception as e:
            print(str(e))
            return (None, False)
