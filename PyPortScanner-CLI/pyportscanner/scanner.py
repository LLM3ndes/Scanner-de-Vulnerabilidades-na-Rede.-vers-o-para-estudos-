import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(ip, port, timeout=1.0):
    """Tenta conectar em uma porta TCP especifica de um IP.
    Retorna um dicionario com as informacoes do resultado.
    """
    result = {
        "ip": ip,
        "port": port,
        "status": "closed",
        "banner": None,
        "response_time": None
    }
    
    start_time = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    try:
        connection = s.connect_ex((ip, port))
        if connection == 0:
            elapsed = time.time() - start_time
            result["status"] = "open"
            result["response_time"] = round(elapsed, 4)
    except Exception:
        pass
    finally:
        s.close()
        
    return result


def scan_targets_concurrent(targets, ports, max_workers=100, timeout=1.0):
    """Gerencia a varredura concorrente de multiplos alvos e portas usando threads."""
    open_results = []
    completed = 0
    
    print(f"[*] Iniciando varredura em {len(targets)} alvo(s) e {len(ports)} porta(s)...")
    print(f"[*] Usando {max_workers} threads simultaneas.\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for ip in targets:
            for port in ports:
                futures.append(executor.submit(scan_port, ip, port, timeout))
                
        for future in as_completed(futures):
            completed += 1
            res = future.result()
            if res["status"] == "open":
                open_results.append(res)
                print(f"[+] [ABERTA] {res['ip']}:{res['port']} (Tempo: {res['response_time']}s)")
                
    return open_results