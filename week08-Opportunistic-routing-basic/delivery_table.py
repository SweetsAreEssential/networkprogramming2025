import threading
from config import BOOST_AMOUNT, DECAY_FACTOR

class DeliveryTable:
    def __init__(self):
        self.table = {}
        self.lock = threading.Lock()

    def initialize_peer(self, port):
        with self.lock:
            if port not in self.table:
                self.table[port] = 0.5

    def update_success(self, port):
        with self.lock:
            self.table[port] = min(1.0, self.table[port] + BOOST_AMOUNT)

    def update_failure(self, port):
        with self.lock:
            self.table[port] = round(self.table[port] * DECAY_FACTOR, 2)

    def get_candidates(self, threshold):
        with self.lock:
            return [p for p, prob in self.table.items() if prob >= threshold]

    def display(self):
        with self.lock:
            print("\n--- Delivery Probabilities ---")
            for port, prob in self.table.items():
                print(f" Port {port}: {prob}")
            print("------------------------------")