import os
import pytest
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# === RUTAS ABSOLUTAS (siempre relativas al proyecto) ===
ROOT_DIR = Path(__file__).resolve().parents[1]        # .../pruebas-orangehrm
REPORTS_DIR = ROOT_DIR / "reports"
SHOTS_DIR = ROOT_DIR / "screenshots"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SHOTS_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture
def driver():
    chrome_options = Options()
    # Si quieres ver el navegador, comenta la línea siguiente:
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1366,768")
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=chrome_options)
    yield drv
    drv.quit()

# Captura SIEMPRE al final de cada test (pase o falle)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        drv = item.funcargs.get("driver")
        if drv:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{item.name}_{'PASSED' if rep.passed else 'FAILED'}_{ts}.png"
            path = SHOTS_DIR / filename
            ok = False
            try:
                ok = drv.save_screenshot(str(path))
            except Exception as e:
                print(f"[screenshot] Error guardando captura: {e}")
            else:
                print(f"[screenshot] Guardada: {path} (ok={ok})")

def pytest_html_report_title(report):
    report.title = "Reporte de Pruebas - OrangeHRM (Selenium Python)"
