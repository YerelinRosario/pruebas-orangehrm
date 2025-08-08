from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Menú lateral y acciones
    PIM_MENU = (By.XPATH, "//span[normalize-space()='PIM']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    # Formulario Add Employee
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")
    SAVE_BTN = (By.XPATH, "//button[@type='submit']")

    # Confirmaciones / navegación
    TOAST_SUCCESS = (By.XPATH, "//p[contains(normalize-space(),'Success')]")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[normalize-space()='Personal Details']")

    def go_to_pim(self):
        self.wait.until(EC.element_to_be_clickable(self.PIM_MENU)).click()
        # Espera a que cargue la lista (que aparezca el botón Add)
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))

    def add_employee(self, first_name: str, last_name: str, middle_name: str = ""):
        # Estando en módulo PIM
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME)).send_keys(first_name)
        if middle_name:
            self.driver.find_element(*self.MIDDLE_NAME).send_keys(middle_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.SAVE_BTN).click()

    def was_saved_successfully(self) -> bool:
        # Aparece toast de éxito y luego la vista de Personal Details
        try:
            self.wait.until(EC.visibility_of_element_located(self.TOAST_SUCCESS))
        except TimeoutException:
            return False
        try:
            self.wait.until(EC.visibility_of_element_located(self.PERSONAL_DETAILS_HEADER))
            return True
        except TimeoutException:
            return False
