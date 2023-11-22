# import json
# import pytest
# from api.functions.QrCode import QRCodeHandler
# from api.views import QrCodeView
# from rest_framework.test import APIRequestFactory
# from .factories import UserFactory, EventFactory
# from rest_framework import status

# @pytest.mark.django_db
# def test_QRCodeHandler_encrypt_decrypt():
#     # Create a user using the factory
#     user = UserFactory()

#     # Simulate the request
#     factory = APIRequestFactory()
#     request = factory.get("/")
#     request.user = user

#     handler = QRCodeHandler(request)
#     data = b"test_data"
#     encrypted_data = handler._encrypt(data)
#     decrypted_data = handler._decrypt(encrypted_data)

#     assert decrypted_data == data

# @pytest.mark.django_db
# def test_QRCodeHandler_generate():
#     # Create a user using the factory
#     user = UserFactory()

#     # Simulate the request
#     factory = APIRequestFactory()
#     request = factory.get("/")
#     request.user = user

#     handler = QRCodeHandler(request)
#     result = handler.generate()

#     decrypted_result = handler._decrypt(result).decode("utf-8")
#     assert decrypted_result == user.QrUid

# @pytest.mark.django_db
# def test_QRCodeView_get():
#     # Create a user using the factory
#     user = UserFactory()

#     # Simulate the request
#     factory = APIRequestFactory()
#     request = factory.get("/")
#     request.user = user

#     view = QrCodeView.as_view()
#     response = view(request)

#     handler = QRCodeHandler(request)
#     decrypted_response_content = handler._decrypt(response.content).decode("utf-8")
#     assert decrypted_response_content == user.QrUid

# @pytest.mark.django_db
# def test_QRCodeView_post():
#     # Create a user and event using the factories
#     user = UserFactory()
#     event = EventFactory()

#     # Encrypt the QrUid
#     handler = QRCodeHandler(mock_request_get)
#     encrypted_data = handler._encrypt(user.QrUid.encode())

#     # Create the data dictionary with the encrypted data
#     data = {"encryptedqrdata": encrypted_data.decode(), "event": event.pk}

#     # Simulate the request
#     factory = APIRequestFactory()
#     request = factory.post("/", data=json.dumps(data), content_type="application/json")
#     request.user = user

#     view = QrCodeView.as_view()
#     response = view(request)

#     assert response.status_code == status.HTTP_202_ACCEPTED
