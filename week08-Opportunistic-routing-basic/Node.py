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
q_lock = threading.Lock()

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
        with q_lock:
            if not message_queue:
                continue
            
            best_targets = table.get_candidates(FORWARD_THRESHOLD)
            for msg in message_queue[:]:
                for port in best_targets:
                    if send_packet(port, msg):
                        table.update_success(port)
                        message_queue.remove(msg)
                        break
                    else:
                        table.update_failure(port)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, MY_PORT))
    server.listen(5)
    print(f"[*] Node {MY_PORT} is listening...")
    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        if data:
            print(f"\n[Received] {data}")
            with q_lock:
                message_queue.append(data)
        conn.close()

if __name__ == "__main__":
    for p in PEERS: 
        table.initialize_peer(p)

    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=forward_task, daemon=True).start()

    while True:
        user_input = input(f"Node-{MY_PORT}> ").strip()
        if user_input == "table":
            table.display()
        elif user_input == "queue":
            print(f"Pending messages: {message_queue}")
        elif user_input:
            with q_lock:
                message_queue.append(user_input)