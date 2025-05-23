# main.py
import argparse
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apac_scraper.auth       import init_driver, login_manual
from apac_scraper.extraction import extract_all_pages
from apac_scraper.export     import save_to_excel
from apac_scraper.config     import OUTPUT_FILE

def parse_args():
    p = argparse.ArgumentParser(description="Scrape APACs por período")
    p.add_argument("--start", required=True, help="Data de início (dd/MM/yyyy)")
    p.add_argument("--end",   required=True, help="Data de fim    (dd/MM/yyyy)")
    return p.parse_args()

def run(start_date: str, end_date: str):
    print("Iniciando run()")
    driver = init_driver()
    print("Navegador aberto")
    try:
        login_manual(driver)
        print("Login feito")

        # 1) Abre direto o formulário de Acompanhamento via JS
        js = """
        parent.frames['content'].location.href =
          'https://siga.saude.prefeitura.sp.gov.br/sms/consultaAcompanhamentoLaudo.do'
          + '?method=initUseCase&subsystem=apac';
        """
        driver.execute_script(js)
        print("Formulário carregado via JS")

        # 2) Vai pro frame de conteúdo
        driver.switch_to.default_content()
        driver.switch_to.frame("content")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "tipoEstabelecimento")))
        print("✔️  Dentro do frame 'content'")

        # 3) Seleciona o rádio “Solicitante E Executante”
        radio = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "input[name='tipoEstabelecimento'][value='solicOuExec']"
        )))
        radio.click()
        print("'Solicitante ou Executante' marcado")

        # 4) Preenche as datas
        inicio = driver.find_element(By.NAME, "dataInicioSolicitacaoCriterium")
        inicio.clear()
        inicio.send_keys(start_date)
        fim = driver.find_element(By.NAME, "dataFimSolicitacaoCriterium")
        fim.clear()
        fim.send_keys(end_date)
        print(f"Datas definidas: {start_date} → {end_date}")

        # 5) Clica em “Consultar”
        consultar = driver.find_element(By.CSS_SELECTOR, "button.bt_consultar")
        consultar.click()
        print("⏳ Consultando…")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.border")))
        print("Resultado carregado")

        # 6) Extrai e salva
        df = extract_all_pages(driver)
        print("💾 Salvando Excel…")
        save_to_excel(df, OUTPUT_FILE)
        print("Pronto!")

    finally:
        driver.quit()
        print("Navegador fechado")

if __name__ == "__main__":
    args = parse_args()
    run(args.start, args.end)
