# tests/pages/pim_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)

    # === Menú lateral y acciones ===
    PIM_MENU = (By.XPATH, "//span[normalize-space()='PIM']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    # === Formulario Add/Personal Details (mismos names) ===
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")   # <- ¡importante que exista!
    LAST_NAME_INPUT  = (By.NAME, "lastName")
    SAVE_BTN         = (By.XPATH, "//button[@type='submit']")

    # === Confirmaciones / navegación ===
    TOAST_SUCCESS = (By.XPATH, "//p[contains(normalize-space(),'Success')]")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[normalize-space()='Personal Details']")

    # --- Navegación al módulo PIM ---
    def go_to_pim(self):
        self.wait.until(EC.element_to_be_clickable(self.PIM_MENU)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))

    # --- Crear empleado ---
    def add_employee(self, first_name: str, last_name: str, middle_name: str = ""):
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT)).send_keys(first_name)
        mid = self.driver.find_element(*self.MIDDLE_NAME_INPUT)
        mid.clear()
        if middle_name:
            mid.send_keys(middle_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.SAVE_BTN).click()

    def was_saved_successfully(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.TOAST_SUCCESS))
            self.wait.until(EC.visibility_of_element_located(self.PERSONAL_DETAILS_HEADER))
            return True
        except TimeoutException:
            return False

    # --- Utilidad: scroll al elemento ---
    def _scroll_into_view(self, locator):
        elem = self.wait.until(EC.visibility_of_element_located(locator))
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
        except Exception:
            pass
        return elem

    # --- HU004: editar nombres en Personal Details ---
    def edit_current_employee_name(self, new_first: str, new_last: str, new_middle: str = "") -> bool:
    # Asegurar que estamos en Personal Details
        self.wait.until(EC.visibility_of_element_located(self.PERSONAL_DETAILS_HEADER))

    # 1) Editar campos de nombre (limpiando middle para evitar validaciones)
        first = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        first.clear(); first.send_keys(new_first)

        middle = self.wait.until(EC.visibility_of_element_located(self.MIDDLE_NAME_INPUT))
        middle.clear()
        if new_middle:
            middle.send_keys(new_middle)

        last = self.wait.until(EC.visibility_of_element_located(self.LAST_NAME_INPUT))
        last.clear(); last.send_keys(new_last)

    # 2) Encontrar el *Save* correcto: el del mismo <form> que contiene firstName
        form = first.find_element(By.XPATH, "./ancestor::form")
        save_btn = form.find_element(By.XPATH, ".//button[@type='submit' and normalize-space()='Save']")

    # 3) Scroll + click con fallback JS (por si hay overlays)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
        except Exception:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable(save_btn)).click()
        except (ElementClickInterceptedException, TimeoutException):
            self.driver.execute_script("arguments[0].click();", save_btn)

    # 4) Confirmar con toast de éxito
        try:
            self.wait.until(EC.visibility_of_element_located(self.TOAST_SUCCESS))
            return True
        except TimeoutException:
            return False
