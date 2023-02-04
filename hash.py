import hashlib


class Hash():
    def __init__(self, data):
        self.data = data
        self.hash: str = self.get_hash()
        
    def get_hash(self) -> str:
        sha = hashlib.sha256()
        sha.update(self.data)
        return sha.hexdigest()