from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


class PublicKey(object):
    def __init__(self, private_key: rsa.RSAPrivateKey = None,
                 public_key: rsa.RSAPublicKey = None, path: str = None,
                 string: str = None, byte_string: bytes = None):
        if private_key is not None and isinstance(private_key,
                                                  rsa.RSAPrivateKey):
            self.key = private_key.public_key()
        elif private_key is not None and isinstance(private_key, PrivateKey):
            private_key: PrivateKey = private_key
            self.key = private_key.public_key.key
        elif path is not None:
            with open(path, "rb") as file:
                union_key = serialization.load_pem_public_key(file.read())
                if isinstance(union_key, rsa.RSAPublicKey):
                    self.key = union_key
        elif string is not None:
            if isinstance(string, str):
                byte_string = bytes(string.encode('ascii'))
            else:
                byte_string = string

            union_key = serialization.load_pem_public_key(byte_string)
            if isinstance(union_key, rsa.RSAPublicKey):
                self.key = union_key
        elif byte_string is not None:

            union_key = serialization.load_pem_public_key(byte_string)
            if isinstance(union_key, rsa.RSAPublicKey):
                self.key = union_key
        elif public_key is not None:
            self.key = public_key

    def get_pem(self):
        pem = self.key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem

    def write(self, path):
        pem = self.get_pem()

        with open(path, 'wb') as file:
            file.write(pem)

    def verify(self, signature: bytes, message: str = None,
               byte_message: bytes = None):
        if message is not None:
            byte_message = bytes(message.encode('ascii'))
        elif byte_message is None:
            raise BaseException('No message to verify')

        try:
            self.key.verify(
                signature,
                byte_message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            return True
        except Exception:
            return False

    def __repr__(self):
        return str(self.get_pem())


class PrivateKey(object):
    def __init__(self, key: rsa.RSAPrivateKey = None, path: str = None,
                 string: str = None, byte_string: bytes = None):
        if key is not None:
            self.key = key
        elif path is not None:
            with open(path, "rb") as file:
                union_key = serialization.load_pem_private_key(file.read(),
                                                               password=None)
                if isinstance(union_key, rsa.RSAPrivateKey):
                    self.key = union_key
        elif string is not None:
            byte_string = bytes(string.encode('ascii'))

            union_key = serialization.load_pem_private_key(byte_string,
                                                           password=None)
            if isinstance(union_key, rsa.RSAPrivateKey):
                self.key = union_key
        elif byte_string is not None:
            union_key = serialization.load_pem_private_key(byte_string,
                                                           password=None)
            if isinstance(union_key, rsa.RSAPrivateKey):
                self.key = union_key
        else:
            self.key = rsa.generate_private_key(public_exponent=65537,
                                                key_size=2048)

        self.public_key = PublicKey(public_key=self.key.public_key())

    def get_pem(self):
        pem = self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        return pem

    def write(self, path):
        pem = self.get_pem()

        with open(path, 'wb') as file:
            file.write(pem)

    def sign(self, message):
        if isinstance(message, str):
            message = bytes(message.encode('ascii'))

        signature = self.key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return signature

# private_key = PrivateKey(path='private_key.pem')
# public_key = PublicKey(byte_string=private_key.public_key.get_pem())

# signature = private_key.sign('Hello, crypto world!')
# print(public_key.verify(signature, 'Hello, crypto world!'))
