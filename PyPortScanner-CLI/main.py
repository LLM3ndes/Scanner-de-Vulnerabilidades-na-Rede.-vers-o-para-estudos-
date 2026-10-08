import ipaddress
import sys
import time

from pyportscanner.banner import estimate_os_by_ttl, grab_banner
from pyportscanner.cli import parse_args, parse_ports
from pyportscanner.reporter import export_json, generate_html_report
from pyportscanner.scanner import scan_targets_concurrent


def resolve_targets(target_str):
    """Converte uma string de IP único ou bloco CIDR em uma lista de IPs válidos."""
    targets = []
    
    try:
        if "/" in target_str:
            net = ipaddress.ip_network(target_str, strict=False)
            targets = [str(ip) for ip in net.hosts()]
        else:
            ip = ipaddress.ip_address(target_str)
            targets = [str(ip)]
    except ValueError as e:
        print(f"[!] Erro de Endereçamento IP: {e}")
        sys.exit(1)
        
    return targets


def main():
    """Funcao principal de orquestracao do PyPortScanner-CLI."""
    args = parse_args()
    targets = resolve_targets(args.target)
    ports = parse_ports(args.ports)
    
    start_time = time.time()
    
    # Executa a varredura concorrente de portas
    results = scan_targets_concurrent(
        targets=targets,
        ports=ports,
        max_workers=args.workers,
        timeout=args.timeout,
    )
    
    # Se a captura de banner estiver ativada, enriquece os resultados das portas abertas
    if args.banner and results:
        print("\n[*] Coletando banners e assinaturas dos servicos encontrados...")
        for item in results:
            print(f"[*] Capturando banner em {item['ip']}:{item['port']}...")
            banner = grab_banner(item["ip"], item["port"], timeout=args.timeout)
            item["banner"] = banner
            
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print(f"[+] Varredura concluida em {elapsed_time:.2f} segundos.")
    print(f"[+] Total de portas abertas encontradas: {len(results)}")
    print("=" * 60 + "\n")
    
    # Exportacao de relatorios
    if args.output:
        filename = args.output
        if filename.endswith(".json"):
            export_json(results, filename)
        elif filename.endswith(".html"):
            generate_html_report(results, args.target, elapsed_time, filename)
        else:
            # Se nao especificar extensao valida, gera ambos por padrao
            export_json(results, f"{filename}.json")
            generate_html_report(
                results, args.target, elapsed_time, f"{filename}.html"
            )


if __name__ == "__main__":
    main()