import requests
from helpers import from_chain
from crypto import PublicKey, PrivateKey
from transaction import Transaction


class Node(object):
    def __init__(self, ip):
        self.ip = ip
        
    def add_transaction(self, transaction: Transaction, from_node: bool):
        pem = transaction.public_key
        if transaction.public_key != '0':
            pem = transaction.public_key.get_pem().decode('ascii')
        if transaction.amount > 0:
            requests.post(self.ip + '/add_transaction', json={'public_key': pem, 'sender': transaction.sender, 'recipient': transaction.recipient, 'amount': transaction.amount, 'signature': str(transaction.signature), 'previous_block_hash': transaction.previous_block_hash, 'from_node': from_node, 'addresses': transaction.addresses, 'time': transaction.time})
    
    def resolve(self, from_node):
        requests.post(self.ip + '/resolve', json={'from_node': from_node})
        
    def chain(self):
        from blockchain import Blockchain, Block, Transaction
        
        chain = requests.get(self.ip + '/chain').json()
        blockchain = from_chain(chain)
        
        return blockchain
        
    def add_node(self, ip):
        requests.post(self.ip + '/add_node', json={'ip': ip})


if __name__ == '__main__':
    from helpers import new_signed_transaction, public_to_address
    
    public_key = PublicKey(path='wallet/public_key_wallet.pem')
    private_key = PrivateKey(path='wallet/private_key_wallet.pem')
    
    #transaction = new_signed_transaction('0', '0', 'cc75643911bc12f81a830e58abdda8293bb674ed', 1, private_key)
    
    #node = Node('http://localhost:4949')
    # node.add_node('http://localhost:4947')
    #node.add_node('http://localhost:4948')
    
    node = Node('http://localhost:4948')
    # node.add_node('http://localhost:4947')
    #node.add_node('http://localhost:4949')
    
    # node = Node('http://localhost:4947')
    # node.add_node('http://localhost:4948')
    # node.add_node('http://localhost:4949')
    
    transaction = new_signed_transaction(public_key, public_to_address(public_key), '7c8888254a6727ceefcedf805b0129f783088fdc', 1, private_key, node)
    node.add_transaction(transaction, False)
