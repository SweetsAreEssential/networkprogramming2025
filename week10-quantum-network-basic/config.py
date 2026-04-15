HOST = "127.0.0.1"
BUFFER_SIZE = 1024
TOKEN_TTL = 30          # ข้อความจะสลายตัว (Expire) ภายใน 30 วินาที
UPDATE_INTERVAL = 1     # เช็คคิวทุก 1 วินาที (Low Latency)
STRICT_NO_CLONE = True  # ถ้าส่งพลาด ข้อความจะถูกทำลายทันที (ห้ามคัดลอก)