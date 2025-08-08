from tests.pages.login_page import LoginPage

def test_login_exitoso(driver):
    page = LoginPage(driver)
    page.open()
    page.login("Admin", "admin123")
    assert page.dashboard_is_visible(), "No se visualizó el Dashboard tras login válido"
