# config.py
HOST = "127.0.0.1"
BUFFER_SIZE = 1024
INITIAL_PHEROMONE = 1.0  # ค่าฟีโรโมนเริ่มต้น
REINFORCEMENT = 0.3      # ค่าที่บวกเพิ่มเมื่อส่งสำเร็จ
DECAY_RATE = 0.9         # อัตราการระเหย (คูณ 0.9 ทุกรอบ)
PHEROMONE_THRESHOLD = 0.5 # ค่าต่ำสุดที่จะยอมส่งต่อ
UPDATE_INTERVAL = 3       # ความเร็วในการเช็คคิว (วินาที)