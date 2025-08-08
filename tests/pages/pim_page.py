# tests/pages/pim_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)

    # ===== Menú y acciones =====
    PIM_MENU = (By.XPATH, "//span[normalize-space()='PIM']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    # ===== Campos de Personal Details / Add Employee =====
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT  = (By.NAME, "lastName")
    SAVE_BTN         = (By.XPATH, "//button[@type='submit']")

    # ===== Confirmaciones / navegación =====
    TOAST_SUCCESS = (By.XPATH, "//p[contains(normalize-space(),'Success')]")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[normalize-space()='Personal Details']")

    # --- Navegar a PIM ---
    def go_to_pim(self):
        self.wait.until(EC.element_to_be_clickable(self.PIM_MENU)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))

    # --- Crear empleado (HU003) ---

    def add_employee(self, first_name: str, last_name: str, middle_name: str = ""):
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT)).send_keys(first_name)
    
        mid = self.driver.find_element(*self.MIDDLE_NAME_INPUT)
        mid.clear()
        if middle_name:
            mid.send_keys(middle_name)

        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

        # >>>>>>> FIX: evitar "Employee Id already exists"
        eid = self.wait.until(EC.visibility_of_element_located(self.EMPLOYEE_ID_INPUT))
        eid.clear()  # opción 1: dejarlo vacío para que el sistema asigne
        # O si prefieres forzar uno único, usa esto:
        # eid.send_keys(f"{int(time.time())%1000000:06d}")

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

    # --- HU004: Actualizar nombre(s) en Personal Details ---
    def edit_current_employee_name(self, new_first: str, new_last: str, new_middle: str = "") -> bool:
        # Asegurar que estamos en Personal Details
        self.wait.until(EC.visibility_of_element_located(self.PERSONAL_DETAILS_HEADER))

        # 1) Editar campos (limpia middle para evitar validaciones >30 chars)
        first = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        first.clear(); first.send_keys(new_first)

        middle = self.wait.until(EC.visibility_of_element_located(self.MIDDLE_NAME_INPUT))
        middle.clear()
        if new_middle:
            middle.send_keys(new_middle)

        last = self.wait.until(EC.visibility_of_element_located(self.LAST_NAME_INPUT))
        last.clear(); last.send_keys(new_last)

        # 2) Encontrar el Save correcto dentro del mismo <form> de nombres
        form = first.find_element(By.XPATH, "./ancestor::form")
        save_btn = form.find_element(By.XPATH, ".//button[@type='submit' and normalize-space()='Save']")

        # 3) Scroll + click con fallback JS
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
        except Exception:
            pass
        try:
            self.wait.until(EC.element_to_be_clickable(save_btn)).click()
        except (ElementClickInterceptedException, TimeoutException):
            self.driver.execute_script("arguments[0].click();", save_btn)

        # 4) Validación dual: toast o valores persistidos en inputs
        try:
            self.wait.until(EC.visibility_of_element_located(self.TOAST_SUCCESS))
            return True
        except TimeoutException:
            try:
                self.wait.until(EC.text_to_be_present_in_element_value(self.FIRST_NAME_INPUT, new_first))
                self.wait.until(EC.text_to_be_present_in_element_value(self.LAST_NAME_INPUT, new_last))
                return True
            except TimeoutException:
                return False
    



        # ===== Filtros / Lista =====
        # ===== Filtros / Lista =====
    EMPLOYEE_NAME_FILTER = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
    EMPLOYEE_ID_INPUT = (By.XPATH, "//label[normalize-space()='Employee Id']/../following-sibling::div//input")
    SUGGESTION_ITEM     = (By.XPATH, "//div[@role='listbox']//span")
    SEARCH_BTN          = (By.XPATH, "//button[normalize-space()='Search']")
    TABLE_BODY          = (By.CSS_SELECTOR, "div.oxd-table-body")
    FIRST_ROW           = (By.XPATH, "//div[contains(@class,'oxd-table-body')]/div[contains(@class,'oxd-table-card')][1]")
    

    # ===== Acciones en la fila / barra superior =====
    ROW_CHECKBOX_FIRST  = (By.XPATH, "//div[contains(@class,'oxd-table-body')]/div[1]//i[contains(@class,'bi-check')]")
    ROW_TRASH_FIRST     = (By.XPATH, "//div[contains(@class,'oxd-table-body')]/div[1]//i[contains(@class,'bi-trash')]")
    TOPBAR_DELETE_BTN   = (By.XPATH, "//div[contains(@class,'orangehrm-header-container')]//button[.//i[contains(@class,'bi-trash')]]")

    # ===== Modal de confirmación =====
    CONFIRM_DELETE_BTN  = (By.XPATH, "//button[normalize-space()='Yes, Delete']")
    # (TOAST_SUCCESS ya lo tienes definido arriba)

    def search_employee_by_name_exact(self, name: str):
        """Escribe el nombre en el filtro, selecciona la sugerencia y busca."""
        box = self.wait.until(EC.visibility_of_element_located(self.EMPLOYEE_NAME_FILTER))
        box.clear()
        box.send_keys(name)
        # seleccionar sugerencia exacta
        self.wait.until(EC.visibility_of_element_located(self.SUGGESTION_ITEM)).click()
        # buscar
        self.driver.find_element(*self.SEARCH_BTN).click()
        # esperar al menos una fila
        self.wait.until(EC.visibility_of_element_located(self.FIRST_ROW))
    
    def delete_first_result(self) -> bool:
        """Marca la primera fila y elimina. Si hay icono de papelera por fila lo usa; si no, usa el Delete de la barra superior."""
        # 1) Intentar borrar con el ícono de la primera fila
        try:
            self.wait.until(EC.element_to_be_clickable(self.ROW_TRASH_FIRST)).click()
        except Exception:
            # 2) Si no hay ícono por fila, usa el checkbox + botón Delete de la barra superior
            self.wait.until(EC.element_to_be_clickable(self.ROW_CHECKBOX_FIRST)).click()
            self.wait.until(EC.element_to_be_clickable(self.TOPBAR_DELETE_BTN)).click()
    
        # 3) Confirmar en el modal
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BTN)).click()
    
        # 4) Ver toast de éxito
        try:
            self.wait.until(EC.visibility_of_element_located(self.TOAST_SUCCESS))
            return True
        except TimeoutException:
            return False

