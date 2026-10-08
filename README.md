# 🛡️ PyPortScanner

Um scanner de portas TCP de alta performance e capturador de banners escrito em Python, com saída no terminal em tempo real e relatórios em HTML5/JSON.

---

## 📌 Funcionalidades

- **Varredura Multithreaded:** Execução de conexões em paralelo utilizando `ThreadPoolExecutor`.
- **Alvos Flexíveis:** Aceita endereços IPv4 únicos ou blocos CIDR (ex: `192.168.1.0/24`).
- **Intervalos de Portas Personalizados:** Suporta listas (`22,80,443`), intervalos (`1-1024`) ou combinações.
- **Captura de Banners de Serviços:** Identifica assinaturas em portas abertas (HTTP, SSH, FTP, etc.).
- **Relatórios Automatizados:** Gera saídas estruturadas em **JSON** e relatórios modernos em **HTML5/CSS3**.

---

## 📂 Estrutura do Projeto

```text
PyPortScanner-CLI/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── pyportscanner/
    ├── __init__.py
    ├── cli.py
    ├── scanner.py
    ├── banner.py
    └── reporter.py
