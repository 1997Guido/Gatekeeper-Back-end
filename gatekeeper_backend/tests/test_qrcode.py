import json
import pytest
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from api.functions.QrCode import QRCodeHandler
from api.views import QrCodeApi
from api.models import User, Event, Image
from unittest.mock import PropertyMock
from cryptography.fernet import Fernet


@pytest.fixture
def mock_user():
    return User(pk=1, QrUid="1234567891234567891234567892123456789", ProfilePicture_id=None)

@pytest.fixture
def mock_request_get(mock_user):
    factory = APIRequestFactory()
    request = factory.get('/')
    request.user = mock_user
    return request

@pytest.fixture
def mock_request_post(mock_user):
    data = {
        "encryptedqrdata": "123456789123456789123456789123456789",
        "event": 1
    }
    factory = APIRequestFactory()
    request = factory.post('/', data=json.dumps(data), content_type='application/json')
    request.user = mock_user
    return request

def test_QRCodeHandler_encrypt_decrypt(mock_request_get):
    handler = QRCodeHandler(mock_request_get)

    data = b"test_data"
    encrypted_data = handler._encrypt(data)
    decrypted_data = handler._decrypt(encrypted_data)

    assert decrypted_data == data

def test_QRCodeHandler_generate(mocker, mock_request_get, mock_user):
    mocker.patch('api.functions.QrCode.User.objects.get', return_value=mock_user)

    handler = QRCodeHandler(mock_request_get)
    result = handler.generate()
    
    decrypted_result = handler._decrypt(result).decode("utf-8")
    assert decrypted_result == mock_user.QrUid

def test_QRCodeApi_get(mocker, mock_request_get, mock_user):
    mocker.patch('api.functions.QrCode.User.objects.get', return_value=mock_user)

    view = QrCodeApi.as_view()
    response = view(mock_request_get)

    qr_handler = QRCodeHandler(mock_request_get)
    decrypted_response_content = qr_handler._decrypt(response.content).decode("utf-8")
    assert decrypted_response_content == mock_user.QrUid
   
# Helper function for encrypting data with a mock key 
def encrypt_with_mock_key(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8')).decode('utf-8')

# This is a helper function to get the mock key
def get_mock_key():
    return b"rTFB13nkI4mt76RMiJOpoNZS_aa5LUNyJIJ4BPlbPEY="

# This is the custom __init__ method
def mock_qrcodehandler_init(self, request):
    self.request = request
    self.key = get_mock_key()

def test_QRCodeApi_post(mocker, mock_user):
    mock_event = Event(pk=1)
    mocker.patch('api.functions.QrCode.Event.objects.get', return_value=mock_event)
    mocker.patch('api.functions.QrCode.User.objects.get', return_value=mock_user)
    
    # Mocking the get_guests property to return a guest list containing our mock user
    mocked_get_guests = mocker.patch.object(Event, 'get_guests', new_callable=PropertyMock)
    mocked_get_guests.return_value = [{"id": mock_user.pk}]
    
    # Mock the QRCodeHandler's __init__ method
    mocker.patch.object(QRCodeHandler, '__init__', mock_qrcodehandler_init)
    
    # Encrypt the QrUid using the mock key
    encrypted_data = encrypt_with_mock_key(mock_user.QrUid, get_mock_key())
    
    # Create the data dictionary with the encrypted data
    data = {
        "encryptedqrdata": encrypted_data,
        "event": 1
    }

    # Create the mock_request_post using the data dictionary
    factory = APIRequestFactory()
    mock_request_post = factory.post('/', data=json.dumps(data), content_type='application/json')
    mock_request_post.user = mock_user

    view = QrCodeApi.as_view()
    response = view(mock_request_post)

    assert response.status_code == status.HTTP_202_ACCEPTED