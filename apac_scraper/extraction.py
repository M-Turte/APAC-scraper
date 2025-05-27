# extraction.py

import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TABLE_SELECTOR = "table.border"

def extract_all_pages(driver, timeout: int = 10) -> pd.DataFrame:
    """
    Extrai todas as páginas de APACs: itera
    clicando em “próxima página” até não encontrar mais,
    acumulando somente as páginas que contenham “Nr. APAC”.
    Usa stale-element e comparação de HTML para garantir
    que cada página seja nova.
    """
    dfs = []
    wait = WebDriverWait(driver, timeout)

    # garante que estamos no frame 'content'
    driver.switch_to.default_content()
    driver.switch_to.frame("content")

    page = 1
    while True:
        print(f"\n— Página {page} —")

        # aguarda e coleta todas as tables com class="border"
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, TABLE_SELECTOR)))
        tables = driver.find_elements(By.CSS_SELECTOR, TABLE_SELECTOR)
        if not tables:
            print("❌ Não encontrei nenhuma tabela nesta página.")
        else:
            # escolhe tabela de resultados pela maior # de <tr>
            table = max(tables, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
            html_before = table.get_attribute("outerHTML")
            df_raw = pd.read_html(html_before, flavor="lxml", header=None)[0]
            print(f"  Linhas brutas: {df_raw.shape[0]}")

            # tenta localizar o cabeçalho "Nr. APAC"
            mask = df_raw.eq("Nr. APAC").any(axis=1)
            if mask.any():
                idx = mask.idxmax()
                header = df_raw.iloc[idx].tolist()
                df_page = df_raw.iloc[idx+1 :].copy()
                df_page.columns = header
                print(f"  Carregados {df_page.shape[0]} registros após cabeçalho.")
                dfs.append(df_page)
            else:
                print("⚠️  Cabeçalho 'Nr. APAC' não encontrado; pulando página.")

        # tenta avançar
        try:
            # tenta imagem “on” primeiro, depois “off”
            try:
                img = driver.find_element(By.CSS_SELECTOR, "img[src*='bt_proximo1_on.gif']")
            except NoSuchElementException:
                img = driver.find_element(By.CSS_SELECTOR, "img[src*='bt_proximo1.gif']")
            link = img.find_element(By.XPATH, "./ancestor::a[1]")
            print("⏭️ Clicando em próxima página…")

            # robust wait: stale + HTML diferente
            link.click()
            wait.until(EC.staleness_of(table))
            wait.until(lambda d: d.find_element(By.CSS_SELECTOR, TABLE_SELECTOR)
                               .get_attribute("outerHTML") != html_before)
            time.sleep(0.5)  # opcional
            page += 1

        except (NoSuchElementException, TimeoutException):
            print("🔚 Botão de próxima página não encontrado ou timeout. Finalizando.")
            break

    # concatena tudo
    if dfs:
        full = pd.concat(dfs, ignore_index=True)
        before = full.shape[0]
        full = full.dropna(how='all').reset_index(drop=True)
        removed = before - full.shape[0]
        if removed:
            print(f"🚮 Removidas {removed} linhas vazias.")
        print(f"\n✅ Total: {full.shape[0]} registros em {len(dfs)} páginas válidas.")
        return full
    else:
        print("⚠️  Nenhum dado válido coletado.")
        return pd.DataFrame()
