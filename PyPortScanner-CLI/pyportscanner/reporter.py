import json
import os
import time


def export_json(results, filepath):
    """Exporta os resultados da varredura para um arquivo no formato JSON."""
    data = {
        "scanner": "PyPortScanner-CLI",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_open_ports": len(results),
        "results": results
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"[+] Relatorio JSON salvo com sucesso em: {filepath}")


def generate_html_report(results, target, elapsed_time, filepath):
    """Gera um relatorio visual em HTML5 e CSS3 com os resultados da varredura."""
    rows_html = ""
    for r in results:
        banner_text = r.get("banner") if r.get("banner") else "N/A"
        rows_html += f"""
        <tr>
            <td>{r['port']}</td>
            <td>TCP</td>
            <td>ABERTA</td>
            <td>{r['response_time']}s</td>
            <td>{banner_text}</td>
        </tr>
        """
        
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>PyPortScanner Report</title>
</head>
<body>
    <h1>🛡️ PyPortScanner Report</h1>
    <p>Alvo Escaneado: {target} | Data: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div>
        <p>Portas Abertas: {len(results)}</p>
        <p>Tempo Decorrido: {elapsed_time:.2f}s</p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Porta</th>
                <th>Protocolo</th>
                <th>Estado</th>
                <th>Tempo de Resposta</th>
                <th>Banner / Servico</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</body>
</html>
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print(f"[+] Relatorio HTML5 gerado com sucesso em: {filepath}")