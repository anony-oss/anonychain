from crypto import PublicKey, PrivateKey
from hash import Hash


class Transaction():
    def __init__(self, public_key: PublicKey, sender: str, recipient: str,
                 amount: float, signature: bytes, time: float, previous_block_hash: str):
        self.public_key = public_key
        self.sender = sender
        self.recipient = recipient
        self.amount = int(amount)
        self.signature: bytes = signature
        self.addresses: dict[str, float] = {}
        self.time: float = time
        self.previous_block_hash = previous_block_hash

    def get_address(self, is_sender: bool = True):
        if is_sender:
            return -self.amount
        else:
            return self.amount

    def is_valid(self):
        from helpers import public_to_address
        return self.public_key == '0' or \
                (public_to_address(self.public_key) == self.sender and self.public_key.verify(self.signature, self.get_message()))

    def get_message(self):
        return f'{self.sender}|{self.recipient}|{self.amount}|{self.time}|{self.previous_block_hash}'

    def sign(self, private_key: PrivateKey):
        self.signature = private_key.sign(self.get_message())

    def get_hash(self):
        return Hash(self.get_message()).hash
    
    def hash(self):
        self.transaction_hash = self.get_hash()

    def __repr__(self):
        return f'{self.get_message()}|{self.signature}'

