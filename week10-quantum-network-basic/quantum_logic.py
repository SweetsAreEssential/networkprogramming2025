import time
import uuid

class QuantumToken:
    def __init__(self, message, ttl):
        self.id = str(uuid.uuid4())[:8]
        self.payload = message
        self.expiry = time.time() + ttl
        self.state = "PENDING"

    def is_valid(self):
        if self.state == "PENDING" and time.time() > self.expiry:
            self.state = "EXPIRED"
        return self.state == "PENDING"

    def consume(self):
        """State Collapse: อ่านแล้วสถานะเปลี่ยนทันทีและถาวร"""
        if self.is_valid():
            self.state = "CONSUMED"
            return self.payload
        return None

    def destroy(self):
        self.state = "DESTROYED"

    def __str__(self):
        return f"Token[{self.id}] Status:{self.state} | {self.payload}"