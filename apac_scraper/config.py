# config.py

# Base da aplicação
BASE_URL      = "https://siga.saude.prefeitura.sp.gov.br"

# URLs principais
LOGIN_URL     = BASE_URL + "/sms/login.do"
MENU_PAGE     = BASE_URL + "/sms/index.jsp"

# Endpoint real usado pelo scraper automático (JS ou para montar requisição POST)
API_ENDPOINT  = "/sms/consultaAcompanhamentoLaudo.do"

# Período padrão (pode ser sobrescrito)
DEFAULT_START = "01/05/2025"
DEFAULT_END   = "16/05/2025"

# Tempo padrão para WebDriverWait (em segundos)
DEFAULT_TIMEOUT = 10

# Onde salvar o Excel — se quiser um caminho absoluto, forneça-o aqui
# OUTPUT_FILE = r"C:\Users\mvl_t\PycharmProjects\APAC\apacs_siga.xlsx"
#
# Ou use relativo ao diretório de trabalho atual:
OUTPUT_FILE   = "apacs_siga.xlsx"
