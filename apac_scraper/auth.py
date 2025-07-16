# auth.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .config import LOGIN_URL

def init_driver(headless: bool = False):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless")
    # usa webdriver-manager para garantir a versão compatível do ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=opts)
    driver.maximize_window()
    return driver

def login_manual(driver):
    driver.get(LOGIN_URL)
    input("🔒 Faça login (usuário, senha, CAPTCHA) e aperte ENTER…")