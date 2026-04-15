import socket, threading, time, sys
from config import *
from pheromone_manager import PheromoneManager

MY_PORT = int(sys.argv[1])
PEER_PORTS = [int(p) for p in sys.argv[2:]]

ph_manager = PheromoneManager()
msg_queue = []
seen_cache = set()
data_lock = threading.Lock()

def send_to_peer(port, msg):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((HOST, port))
            s.sendall(msg.encode())
            return True
    except:
        return False

def ant_colony_forwarder():
    """Logic การส่งต่อแบบมด: ระเหยฟีโรโมนและเลือกเส้นทางที่เข้มข้น"""
    while True:
        time.sleep(UPDATE_INTERVAL)
        ph_manager.evaporate()
        
        with data_lock:
            if not msg_queue: continue
            current_tasks = list(msg_queue)
            targets = ph_manager.select_best_routes(PHEROMONE_THRESHOLD)

        for msg in current_tasks:
            for port in targets:
                if send_to_peer(port, msg):
                    ph_manager.add_pheromone(port) # Reinforce path
                    with data_lock:
                        if msg in msg_queue: msg_queue.remove(msg)
                    break

def start_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, MY_PORT))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            data = conn.recv(BUFFER_SIZE).decode()
            if data:
                with data_lock:
                    if data not in seen_cache:
                        print(f"\n[INCOMING] {data}\nNode-{MY_PORT}> ", end="")
                        msg_queue.append(data)
                        seen_cache.add(data)
            conn.close()

if __name__ == "__main__":
    for p in PEER_PORTS: ph_manager.add_pheromone(p, INITIAL_PHEROMONE)
    threading.Thread(target=start_listener, daemon=True).start()
    threading.Thread(target=ant_colony_forwarder, daemon=True).start()

    while True:
        cmd = input(f"Node-{MY_PORT}> ").strip()
        if cmd == "status": print(f"Pheromones: {ph_manager.dump()}")
        elif cmd:
            ts_msg = f"{cmd} (id:{int(time.time())})" # กัน Loop และส่งซ้ำได้
            with data_lock:
                msg_queue.append(ts_msg)
                seen_cache.add(ts_msg)