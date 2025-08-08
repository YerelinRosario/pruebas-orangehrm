import pytest
from tests.pages.login_page import LoginPage

@pytest.mark.parametrize(
    "user,pwd",
    [
        ("Admin", "wrongpass"),   # contraseña incorrecta
        ("WrongUser", "admin123") # usuario incorrecto
    ],
)
def test_login_invalido_muestra_mensaje_y_no_entra(driver, user, pwd):
    page = LoginPage(driver)
    page.open()
    page.login(user, pwd)

    # 1) Aparece el mensaje de error
    assert page.get_error_text().strip() == "Invalid credentials", "No apareció el mensaje 'Invalid credentials'"

    # 2) No debe ir al Dashboard
    assert page.dashboard_is_not_visible(), "Se mostró el Dashboard pese a credenciales inválidas"

    # 3) (extra) Sigue en la página de login
    assert page.url_contains("/auth/login"), "La URL no es de login tras intento inválido"
