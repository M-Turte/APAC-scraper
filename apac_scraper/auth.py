# auth.py
from selenium import webdriver
from .config import LOGIN_URL

def init_driver(headless: bool = False):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    return driver

def login_manual(driver):
    driver.get(LOGIN_URL)
    input("🔒 Faça login (usuário, senha, CAPTCHA) e aperte ENTER…")
