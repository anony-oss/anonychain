from crypto import PublicKey, PrivateKey
from blockchain import Blockchain, Transaction
from helpers import new_signed_transaction, public_to_address


john_private = PrivateKey()
john = PublicKey(private_key=john_private)
john_address = public_to_address(john)

bob_private = PrivateKey()
bob = PublicKey(private_key=bob_private)
bob_address = public_to_address(bob)

alice_private = PrivateKey()
alice = PublicKey(private_key=alice_private)
alice_address = public_to_address(alice)

jack_private = PrivateKey()
jack = PublicKey(private_key=jack_private)
jack_address = public_to_address(jack)


blockchain = Blockchain([], 5, 'cc75643911bc12f81a830e58abdda8293bb674ed')

blockchain.add_transaction([
        Transaction('0', '0', bob_address, 1, '0', blockchain.chain[-1].hash),
        new_signed_transaction(bob, bob_address, alice_address, 1,
                               bob_private, blockchain.chain[-1].hash)
])
blockchain.new_block()

blockchain.add_transaction([
        Transaction('0', '0', alice_address, 1, '0',
                    blockchain.chain[-1].hash),
        new_signed_transaction(alice, alice_address, bob_address, 0.4,
                               alice_private, blockchain.chain[-1].hash)
])
blockchain.new_block()

blockchain.add_transaction([
        Transaction('0', '0', jack_address, 1, '0', blockchain.chain[-1].hash),
        new_signed_transaction(jack, jack_address, bob_address, 0.9,
                               jack_private, blockchain.chain[-1].hash)
])
blockchain.new_block()

blockchain.add_transaction([
        Transaction('0', '0', john_address, 1, '0', blockchain.chain[-1].hash),
        new_signed_transaction(bob, bob_address, jack_address, 1, bob_private,
                               blockchain.chain[-1].hash)
])
blockchain.new_block()

blockchain.add_transaction(Transaction('0', '0', john_address, 1, '0',
                                       blockchain.chain[-1].hash))
blockchain.new_block()

blockchain.add_transaction(Transaction('0', '0', john_address, 1, '0',
                                       blockchain.chain[-1].hash))
blockchain.new_block()

blockchain.add_transaction([
        Transaction('0', '0', john_address, 1, '0', blockchain.chain[-1].hash),
        new_signed_transaction(john, john_address, alice_address, 3.5,
                               john_private, blockchain.chain[-1].hash)
])
blockchain.new_block()

print(blockchain.chain[-1].transaction_base.addresses)
