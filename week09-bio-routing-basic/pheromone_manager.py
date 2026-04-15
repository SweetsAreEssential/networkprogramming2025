import threading
from config import DECAY_RATE, REINFORCEMENT

class PheromoneManager:
    def __init__(self):
        self.table = {}
        self.lock = threading.Lock()

    def add_pheromone(self, port, amount=REINFORCEMENT):
        with self.lock:
            self.table[port] = self.table.get(port, 0.0) + amount

    def evaporate(self):
        """จำลองการระเหยของฟีโรโมนตามกาลเวลา"""
        with self.lock:
            for port in self.table:
                self.table[port] = round(self.table[port] * DECAY_RATE, 2)

    def select_best_routes(self, threshold):
        with self.lock:
            return [p for p, v in self.table.items() if v >= threshold]

    def dump(self):
        with self.lock:
            return str(self.table)