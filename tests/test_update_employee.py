import time
from tests.pages.login_page import LoginPage
from tests.pages.pim_page import PIMPage

def test_actualizar_empleado(driver):
    # 1) Login
    login = LoginPage(driver)
    login.open()
    login.login("Admin", "admin123")
    assert login.dashboard_is_visible(), "No entró al Dashboard tras login"

    # 2) Crear empleado para asegurar que existe
    pim = PIMPage(driver)
    pim.go_to_pim()

    timestamp = time.strftime("%Y%m%d%H%M%S")
    first = "Auto"
    last = f"Updater{timestamp}"
    pim.add_employee(first, last)
    assert pim.was_saved_successfully(), "No se guardó el empleado inicial"

    # 3) Editar (UPDATE) con nombres cortos para no pasar los 30 caracteres
    timestamp_short = time.strftime("%H%M%S")
    new_first = f"Edit{timestamp_short}"
    new_last  = f"User{timestamp_short}"
    assert pim.edit_current_employee_name(new_first, new_last), "No se guardaron los cambios de nombre/apellido"

