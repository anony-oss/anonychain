import time
import secrets
from hash import Hash

class Miner(object):
    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        
    def hash(self, data: str):
        return Hash(data.encode('ascii')).hash
        
    def mine(self, data):
        salt = 0
        
        while not self.hash(data + '|' + str(salt)).endswith('0' * self.difficulty):
            salt += 1
        print(f'Hash: {self.hash(data + "|" + str(salt))}')
        
        return salt
    
if __name__ == '__main__':
    hashes = 0
    full_start = time.perf_counter()
    for i in range(1, 10):
        miner = Miner(i)
        current = 0
        
        print()
        print()
        print(f'Difficulty: {i}')
        for j in range(3):
            start = time.perf_counter()
            hashes += miner.mine(secrets.token_urlsafe(16))
            end = time.perf_counter()
            current += end - start
            print(f'Time for {j} block: {end - start}')
            print(f'Hashrate: {hashes / (time.perf_counter() - full_start)}')
            print(f'Success hashrate: {1 / (current / 3)}')
            print()