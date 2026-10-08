import argparse
import sys


def parse_args():
    """Configura e valida os argumentos de linha de comando para o PyPortScanner-CLI."""
    parser = argparse.ArgumentParser(
        description="PyPortScanner-CLI - Scanner de Portas e Banner Grabbing Multithreaded",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-t", "--target",
        type=str,
        required=True,
        help="IP ou bloco CIDR do alvo (ex: 192.168.1.1 ou 10.0.0.0/24)"
    )
    parser.add_argument(
        "-p", "--ports",
        type=str,
        default="1-1024",
        help="Intervalo de portas ou lista separada por virgula (ex: 80,443,8080 ou 1-65535).\nPadrao: 1-1024"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100,
        help="Numero maximo de threads concorrentes (padrao: 100)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout de conexao em segundos por porta (padrao: 1.0)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Caminho do arquivo para salvar o relatorio (ex: relatorio.json ou relatorio.html)"
    )
    parser.add_argument(
        "--banner",
        action="store_true",
        help="Ativa a captura de banner/assinatura dos servicos nas portas abertas"
    )
    return parser.parse_args()


def parse_ports(ports_str):
    """Converte a string de portas fornecida pelo usuario em uma lista de inteiros validos.
    Suporta formatos: "80,443", "1-100", ou combinacoes como "22,80,100-200".
    """
    ports = set()
    parts = ports_str.split(",")
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if "-" in part:
            try:
                start, end = part.split("-")
                start_int, end_int = int(start), int(end)
                
                if 1 <= start_int <= 65535 and 1 <= end_int <= 65535:
                    ports.update(range(start_int, end_int + 1))
                else:
                    print(f"[!] Erro: Intervalo de portas invalido '{part}'. Use 1-65535.")
                    sys.exit(1)
            except ValueError:
                print(f"[!] Erro: Formato de intervalo invalido '{part}'.")
                sys.exit(1)
        else:
            try:
                port_int = int(part)
                if 1 <= port_int <= 65535:
                    ports.add(port_int)
                else:
                    print(f"[!] Erro: Porta fora do intervalo valido (1-65535): {part}")
                    sys.exit(1)
            except ValueError:
                print(f"[!] Erro: Valor de porta invalido '{part}'.")
                sys.exit(1)
                
    return sorted(list(ports))