import time
from tests.pages.login_page import LoginPage
from tests.pages.pim_page import PIMPage

def test_crear_empleado_camino_feliz(driver):
    # 1) Login
    login = LoginPage(driver)
    login.open()
    login.login("Admin", "admin123")
    assert login.dashboard_is_visible(), "No entró al Dashboard tras login"

    # 2) Navegar a PIM y crear empleado con datos únicos
    pim = PIMPage(driver)
    pim.go_to_pim()

    timestamp = time.strftime("%Y%m%d%H%M%S")
    first = "Auto"
    last = f"Tester{timestamp}"

    pim.add_employee(first, last)

    # 3) Verificaciones mínimas: toast + redirección a Personal Details
    assert pim.was_saved_successfully(), "No apareció confirmación de guardado o 'Personal Details'"

    # (Opcional: aquí podrías agregar asserts extra, como verificar que la URL contiene '/pim/viewPersonalDetails')
