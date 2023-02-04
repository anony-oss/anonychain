from crypto import PrivateKey
from helpers import public_to_address

private_key = PrivateKey()
public_key = private_key.public_key
address = public_to_address(public_key)

private_key.write('./private_key_wallet.pem')
public_key.write('./public_key_wallet.pem')
with open('./address_wallet.txt', 'w') as file:
    file.write(address)
