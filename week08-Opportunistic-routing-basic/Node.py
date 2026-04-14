import socket
import threading
import time
import sys
from config import HOST, BUFFER_SIZE, FORWARD_THRESHOLD, UPDATE_INTERVAL
from delivery_table import DeliveryTable

MY_PORT = int(sys.argv[1])
PEERS = [int(p) for p in sys.argv[2:]]

table = DeliveryTable()
message_queue = []
seen_messages = set()
lock = threading.Lock()

def send_packet(target_port, msg):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((HOST, target_port))
            s.sendall(msg.encode())
            return True
    except:
        return False

def forward_task():
    while True:
        time.sleep(UPDATE_INTERVAL)
        
        # คัดลอกข้อมูลออกมาทำงานข้างนอกเพื่อไม่ให้ล็อคค้าง
        with lock:
            if not message_queue: continue
            current_queue = list(message_queue)
            targets = table.get_candidates(FORWARD_THRESHOLD)
        
        for msg in current_queue:
            for port in targets:
                if send_packet(port, msg):
                    with lock:
                        if msg in message_queue: message_queue.remove(msg)
                    table.update_success(port)
                    break
                else:
                    table.update_failure(port)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, MY_PORT))
    server.listen(5)
    print(f"[*] Node {MY_PORT} online. Listening...")
    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data:
            with lock:
                if data not in seen_messages:
                    # พิมพ์ข้อความที่รับได้และขึ้น Prompt ใหม่ทันที
                    print(f"\n[RECV] {data}\nNode-{MY_PORT}> ", end="")
                    message_queue.append(data)
                    seen_messages.add(data)
        conn.close()

if __name__ == "__main__":
    for p in PEERS: table.initialize_peer(p)
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=forward_task, daemon=True).start()

    while True:
        user_input = input(f"Node-{MY_PORT}> ").strip()
        if user_input == "table":
            table.display()
        elif user_input == "queue":
            print(f"Pending: {message_queue}")
        elif user_input:
            # ใช้ Timestamp เพื่อให้แต่ละข้อความ Unique กัน Loop
            ts_msg = f"{user_input} (at {time.strftime('%H:%M:%S')})"
            with lock:
                message_queue.append(ts_msg)
                seen_messages.add(ts_msg)