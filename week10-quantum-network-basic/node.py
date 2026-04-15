import socket, threading, time, sys
from config import *
from quantum_logic import QuantumToken

MY_PORT = int(sys.argv[1])
PEERS = [int(p) for p in sys.argv[2:]]

token_queue = []
token_vault = {} # เก็บประวัติ Token ทั้งหมดที่เคยผ่าน Node นี้
lock = threading.Lock()

def transport_token(target_port, token):
    message = token.consume() # Collapse state locally before sending
    if not message: return False

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((HOST, target_port))
            payload = f"QTOKEN:{token.id}:{message}"
            s.sendall(payload.encode())
            return True
    except:
        if STRICT_NO_CLONE:
            token.destroy() # Failed send kills the token
        return False

def quantum_forwarder():
    while True:
        time.sleep(UPDATE_INTERVAL)
        with lock:
            if not token_queue: continue
            active_queue = [t for t in token_queue if t.is_valid()]
        
        for token in active_queue:
            for peer in PEERS:
                if transport_token(peer, token):
                    with lock:
                        if token in token_queue: token_queue.remove(token)
                    break

def listen_for_tokens():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, MY_PORT))
    server.listen(5)
    print(f"[*] Quantum Node {MY_PORT} is active...")
    while True:
        conn, addr = server.accept()
        raw_data = conn.recv(BUFFER_SIZE).decode()
        if raw_data.startswith("QTOKEN:"):
            _, t_id, msg = raw_data.split(":", 2)
            with lock:
                if t_id not in token_vault:
                    new_token = QuantumToken(msg, TOKEN_TTL)
                    token_queue.append(new_token)
                    token_vault[t_id] = new_token
                    print(f"\n[RECV] Quantum Token {t_id} received.\nNode-{MY_PORT}> ", end="")
        conn.close()

if __name__ == "__main__":
    threading.Thread(target=listen_for_tokens, daemon=True).start()
    threading.Thread(target=quantum_forwarder, daemon=True).start()

    while True:
        cmd = input(f"Node-{MY_PORT}> ").strip()
        if cmd == "history":
            for tid, t in token_vault.items(): print(t)
        elif cmd:
            with lock:
                t = QuantumToken(cmd, TOKEN_TTL)
                token_queue.append(t)
                token_vault[t.id] = t