import time
from tests.pages.login_page import LoginPage
from tests.pages.pim_page import PIMPage

def test_eliminar_empleado(driver):
    # 1) Login
    login = LoginPage(driver)
    login.open()
    login.login("Admin", "admin123")
    assert login.dashboard_is_visible(), "No entró al Dashboard tras login"

    # 2) Crear empleado único
    pim = PIMPage(driver)
    pim.go_to_pim()

    ts = time.strftime("%Y%m%d%H%M%S")
    first = "Del"
    last  = f"Target{ts}"
    full_name = f"{first} {last}"   # OrangeHRM concatena así el filtro

    pim.add_employee(first, last)
    assert pim.was_saved_successfully(), "No se guardó el empleado a eliminar"

    # 3) Volver a lista y buscar por nombre
    pim.go_to_pim()  # regresa a Employee List
    pim.search_employee_by_name_exact(full_name)

    # 4) Borrar primer resultado y validar
    assert pim.delete_first_result(), "No se confirmó el borrado (no apareció toast de éxito)"
