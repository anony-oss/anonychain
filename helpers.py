import hashlib
from crypto import PublicKey
import time


def new_signed_transaction(public_key, sender, recipient, amount, private_key, node):
    from blockchain import Transaction
    
    transaction = Transaction(public_key, sender, recipient, amount, '0', time.time(), node.chain().chain[-1].block_hash)
    transaction.signature = private_key.sign(transaction.get_message())

    return transaction


def public_to_address(public_key: PublicKey):
    sha = hashlib.sha256()
    sha.update(str(public_key.key.public_numbers()).encode('ascii'))
    address = sha.hexdigest()

    ripemd = hashlib.new('ripemd160')
    ripemd.update(str(address).encode('ascii'))
    address = ripemd.hexdigest()
    return address


def check_address(public_key: PublicKey, address: str):
    new_address = public_to_address(public_key)
    return address == new_address

def from_chain(chain: dict):
    from blockchain import Transaction, Blockchain, Block
    from interface import Node
    
    blockchain = Blockchain([], 0, '')
    blockchain.__dict__.update(chain)
    for i, block in enumerate(blockchain.chain):
        blockchain.chain[i] = Block()
        blockchain.chain[i].__dict__.update(block)
        for j, transaction in enumerate(blockchain.chain[i].transactions):
            blockchain.chain[i].transactions[j] = Transaction('0', '0', '0', 0, '0', 0, '0')
            blockchain.chain[i].transactions[j].__dict__.update(transaction)
            if blockchain.chain[i].transactions[j].public_key != '0':
                public_key = PublicKey(string=blockchain.chain[i].transactions[j].public_key)
                blockchain.chain[i].transactions[j].public_key = public_key
        if blockchain.chain[i].previous_block is not None:
            b = Block()
            b.__dict__.update(blockchain.chain[i].previous_block)
            blockchain.chain[i].previous_block = b
    for i, node in enumerate(blockchain.nodes):
        new_node = Node('')
        new_node.ip = node['ip']
        blockchain.nodes[i] = new_node
            
    return blockchain
