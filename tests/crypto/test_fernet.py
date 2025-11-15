import pytest
import random
import base64
from python_plugins.random import secret_token, secret_token_16
from python_plugins.crypto.fernet import generate_fernet_key, fernet_encrypt, fernet_decrypt


class TestFetnet:
    def test_random_secret_token(self):
        token_1 = secret_token()
        # print(token_1)
        assert len(token_1) == 64
        token_2 = secret_token_16()
        # print(token_2)
        assert len(token_2) == 32

    def test_generate_fernet_key(self, fake):
        skey = fake.sentence()
        key = generate_fernet_key(skey)
        # print(key)
        decode_key = base64.urlsafe_b64decode(key)
        # print(decode_key)
        assert len(decode_key) == 32

    def test_fernet_encrypt_decrypt(self, fake):
        key = generate_fernet_key(fake.sentence())
        txt = fake.sentence()
        # print(key,txt)
        token = fernet_encrypt(key, txt)
        # print(token)
        assert isinstance(token, str)
        decrypt_txt = fernet_decrypt(key, token)
        # print(decrypt_txt)
        assert isinstance(decrypt_txt, str)
        assert txt == decrypt_txt

