import os
import time
import pathlib
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEBUG_DIR = pathlib.Path("debug")
DEBUG_DIR.mkdir(exist_ok=True)

URL_LOGIN = "https://gerador.pro/"  # ajuste se o login for outra página

USER = os.getenv("GERADOR_USER", "")
PASS = os.getenv("GERADOR_PASS", "")

def stamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def save_debug(driver, name):
    s = stamp()
    (DEBUG_DIR / f"{name}-{s}.png").write_bytes(driver.get_screenshot_as_png())
    (DEBUG_DIR / f"{name}-{s}.html").write_text(driver.page_source, encoding="utf-8")

def start_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--lang=pt-BR")
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
    opts.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=opts)

def wait_type(driver, by, value, text, t=35):
    el = WebDriverWait(driver, t).until(EC.presence_of_element_located((by, value)))
    el.clear()
    el.send_keys(text)

def wait_click(driver, by, value, t=35):
    el = WebDriverWait(driver, t).until(EC.element_to_be_clickable((by, value)))
    el.click()

def main():
    if not USER or not PASS:
        raise SystemExit("Configure GERADOR_USER e GERADOR_PASS nos Secrets do GitHub.")

    driver = start_driver()
    try:
        driver.get(URL_LOGIN)
        time.sleep(2)
        save_debug(driver, "01-login")

        # ===== AJUSTE (se necessário) =====
        wait_type(driver, By.NAME, "usuario", USER)
        wait_type(driver, By.NAME, "senha", PASS)
        wait_click(driver, By.CSS_SELECTOR, "button[type='submit']")
        # ================================

        time.sleep(3)
        save_debug(driver, "02-apos-login")

        # ===== AJUSTE: entrar no Banner Futebol / Criar Arte =====
        wait_click(driver, By.XPATH, "//div[contains(.,'Banner Futebol')]//a[contains(.,'Criar')]")
        # =========================================================

        time.sleep(3)
        save_debug(driver, "03-area-banner")

        # ===== AJUSTE: aqui você vai clicar em GERAR e depois ENVIAR TELEGRAM =====
        # Exemplo (troque depois que você me mandar o print da tela de gerar):
        # wait_click(driver, By.XPATH, "//button[contains(.,'Gerar')]")
        # time.sleep(5)
        # wait_click(driver, By.XPATH, "//button[contains(.,'Telegram') or contains(.,'Enviar')]")
        # =======================================================================

        print("Cheguei na área do banner. Agora falta ajustar os cliques de GERAR e ENVIAR.")
    except Exception as e:
        print("ERRO:", repr(e))
        try:
            save_debug(driver, "99-erro")
        except:
            pass
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
