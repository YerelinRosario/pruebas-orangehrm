from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    URL = "https://opensource-demo.orangehrmlive.com/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Localizadores
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h6.oxd-text--h6.oxd-topbar-header-breadcrumb-module")

    def open(self):
        self.driver.get(self.URL)

    def login(self, user, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)).send_keys(user)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def dashboard_is_visible(self):
        text = self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER)).text
        return "Dashboard" in text
    
    
    #Intento de login con credenciales incorrectas
    
    
