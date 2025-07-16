# APAC Scraper

Este projeto automatiza a extração de dados de APACs (Autorização de Procedimentos de Alta Complexidade) a partir do sistema SIGA Saúde da Prefeitura de São Paulo, usando Selenium e pandas. O resultado é exportado para:

- **Excel**: `apacs_siga.xlsx`  
- **CSV**:   `apacs_siga.csv`

---

## Descrição

- Realiza login manual (usuário, senha e CAPTCHA).  
- Navega até o formulário de "Acompanhamento de Solicitação".  
- Preenche filtros de período e tipo de estabelecimento.  
- Extrai todas as páginas de resultados automaticamente.  
- Exporta os dados consolidados para arquivos Excel e CSV.

---

## Requisitos

- Python 3.8+  
- Google Chrome instalado  
- **webdriver-manager** (gera e gerencia o ChromeDriver automaticamente)

Dependências (em `requirements.txt`):
```text
selenium
pandas
lxml
openpyxl
beautifulsoup4
requests
webdriver-manager
```

---

##  Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/APAC-scraper.git
   cd APAC-scraper
   ```
2. Crie e ative o virtualenv:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate # macOS/Linux
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

---

##  Estrutura de pastas

```
APAC-scraper/
├── apac_scraper/       # pacote principal
│   ├── __init__.py
│   ├── auth.py         # inicialização do driver e login
│   ├── config.py       # configurações e constantes
│   ├── extraction.py   # extração e paginação
│   ├── export.py       # exportação para Excel
│   ├── main.py         # fluxo automático completo
├── requirements.txt    # dependências
├── .gitignore          # arquivos ignorados pelo Git
└── README.md           # documentação do projeto
```

---

##  Como usar


1. Execute o scraper informando período:

   ```bash
   python -m apac_scraper.main --start dd/MM/yyyy --end dd/MM/yyyy
   ```
2. Faça login manualmente no navegador (aparecerá o prompt).
3. Aguarde até que apacs_siga.xlsx e apacs_siga.csv apareçam na raiz.

---

##  Contribuição

Pull requests são bem-vindos! Para mudanças grandes, abra uma Issue primeiro para discutir o que você gostaria de implementar.


---

**4. Publicar a branch e abrir o Pull Request**  

---

