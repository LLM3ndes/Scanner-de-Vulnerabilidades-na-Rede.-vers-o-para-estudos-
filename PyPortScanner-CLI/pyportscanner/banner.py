import socket


def grab_banner(ip, port, timeout=1.5):
    """Tenta extrair a assinatura/banner do servico rodando na porta."""
    banner = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    try:
        s.connect((ip, port))
        
        # Alguns servicos como HTTP exigem uma requisicao inicial para responder
        if port in [80, 8080, 8000, 8443]:
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        elif port in [21, 22, 25, 110, 143]:
            # FTP, SSH, SMTP enviam banner automaticamente apos conexao
            pass
        else:
            # Envia um byte simples para forcar resposta em outros servicos
            s.sendall(b"\r\n")
            
        response = s.recv(1024)
        if response:
            banner = response.decode("utf-8", errors="ignore").strip()
            if banner:
                banner = banner.split("\n")[0].strip()
    except Exception:
        pass
    finally:
        s.close()
        
    return banner


def estimate_os_by_ttl(ttl):
    """Estima o Sistema Operacional com base no valor TTL (Time To Live)."""
    if ttl is None:
        return "Desconhecido"
    
    if ttl <= 64:
        return "Linux / Unix / Android"
    elif ttl <= 128:
        return "Windows"
    elif ttl <= 255:
        return "Cisco / Roteador"
    else:
        return "Desconhecido"