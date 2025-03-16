from patrolscan.utils import is_valid_license_plate


def test_is_valid_license_plate():
    """
    Prueba la función de validación de matrículas
    """
    assert is_valid_license_plate("ABC123") is True
    assert is_valid_license_plate("") is True
    assert is_valid_license_plate("12345XYZ") is True
