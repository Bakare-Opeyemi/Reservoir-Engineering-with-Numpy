import nbformat
import pytest
import numpy as np
from nbconvert.preprocessors import ExecutePreprocessor


@pytest.mark.parametrize("notebook", ["final_notebook.ipynb"])
def test_notebook_exec(notebook):
    """Test that notebooks execute without errors."""
    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        try:
            assert ep.preprocess(nb) is not None, f"Got empty notebook for {notebook}"
        except Exception:
            assert False, f"Failed executing {notebook}"


def get_notebook_namespace(notebook_path):
    """Execute notebook cells and return namespace with all variables."""
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    namespace = {}
    for cell in nb.cells:
        if cell.cell_type == "code":
            exec(cell.source, namespace)

    return namespace


def test_notebook_variables():
    """Test that notebook variables have expected values."""
    ns = get_notebook_namespace("final_notebook.ipynb")

    # Test 1: Bg_corrected calculation
    assert "Bg_corrected" in ns, "Bg_corrected variable not found"
    Bg_corrected = ns["Bg_corrected"]
    assert isinstance(Bg_corrected, np.ndarray), "Bg_corrected should be numpy array"
    assert len(Bg_corrected) == 5, "Bg_corrected should have 5 elements"
    assert np.all(Bg_corrected > 0), "All Bg values should be positive"
    
    # Verify Bg calculation formula: Bg = (P_sc * T_res * Z) / (T_sc * P_res)
    P_res = np.array([4000, 3500, 3000, 2500, 2000])
    T_res = 180 + 460
    P_sc = 14.7
    T_sc = 60 + 460
    Z = np.array([0.95, 0.92, 0.89, 0.86, 0.83])
    expected_Bg = (P_sc * T_res * Z) / (T_sc * P_res)
    assert np.allclose(Bg_corrected, expected_Bg, rtol=1e-10), "Bg calculation incorrect"

    # Test 2: Havlena-Odeh variables
    assert "F_havlena" in ns, "F_havlena variable not found"
    assert "Eo_havlena" in ns, "Eo_havlena variable not found"
    
    F_havlena = ns["F_havlena"]
    Eo_havlena = ns["Eo_havlena"]
    
    assert isinstance(F_havlena, np.ndarray), "F_havlena should be numpy array"
    assert isinstance(Eo_havlena, np.ndarray), "Eo_havlena should be numpy array"
    assert len(F_havlena) == 5, "F_havlena should have 5 elements"
    assert len(Eo_havlena) == 5, "Eo_havlena should have 5 elements"
    
    # Verify F_havlena calculation: F = Np*Bo + (Gp - Np*Rs)*Bg
    Np = np.array([0, 1.2, 2.8, 4.5, 6.3])
    Bo = np.array([1.45, 1.42, 1.38, 1.35, 1.32])
    Gp = np.array([0, 1.8, 4.5, 8.2, 13.1])
    Rs = np.array([800, 750, 700, 650, 600])
    expected_F = Np * Bo + (Gp * 1000 - Np * Rs) * Bg_corrected
    assert np.allclose(F_havlena, expected_F, rtol=1e-8), "F_havlena calculation incorrect"
    
    # Verify Eo_havlena calculation: Eo = (Bo - Boi) + (Rsi - Rs)*Bg
    Boi = 1.45
    Rsi = 800
    expected_Eo = (Bo - Boi) + (Rsi - Rs) * Bg_corrected
    assert np.allclose(Eo_havlena, expected_Eo, rtol=1e-8), "Eo_havlena calculation incorrect"

    # Test 3: Material balance F values
    assert "F_material_balance" in ns, "F_material_balance variable not found"
    F_material_balance = ns["F_material_balance"]
    assert isinstance(F_material_balance, np.ndarray), "F_material_balance should be numpy array"
    assert len(F_material_balance) == 5, "F_material_balance should have 5 elements"

    # Test 4: Performance prediction
    assert "Np_predicted" in ns, "Np_predicted variable not found"
    Np_predicted = ns["Np_predicted"]
    assert isinstance(Np_predicted, np.ndarray), "Np_predicted should be numpy array"
    assert len(Np_predicted) == 5, "Np_predicted should have 5 elements"
    assert Np_predicted[0] == 0, "Initial Np_predicted should be zero"
    

    # Test 5: Reservoir parameters
    assert "original_oil_in_place" in ns, "original_oil_in_place variable not found"
    assert "gas_cap_ratio" in ns, "gas_cap_ratio variable not found"
    
    original_oil_in_place = ns["original_oil_in_place"]
    gas_cap_ratio = ns["gas_cap_ratio"]
    
    assert isinstance(original_oil_in_place, (int, float, np.number)), "original_oil_in_place should be numeric"
    assert isinstance(gas_cap_ratio, (int, float, np.number)), "gas_cap_ratio should be numeric"
    assert original_oil_in_place > 0, "Original oil in place should be positive"
    assert 0 <= gas_cap_ratio <= 1, "Gas cap ratio should be between 0 and 1"

    # Test 6: Verify material balance consistency
    # For a valid solution, F_material_balance should be close to F_havlena
    # Allow some tolerance for numerical differences
    max_diff = np.max(np.abs(F_material_balance - F_havlena))
    assert max_diff < 10, f"Material balance inconsistency too large: {max_diff}"

    # Test 7: Check that predicted Np is reasonable
    # Predicted Np should be in the same order of magnitude as actual Np
    actual_Np = np.array([0, 1.2, 2.8, 4.5, 6.3])
    if np.any(Np_predicted[1:] > 0):  # Skip first zero element
        ratio = np.mean(Np_predicted[1:] / actual_Np[1:])
        assert 0.1 < ratio < 10, f"Predicted Np seems unreasonable, ratio: {ratio}"



if __name__ == "__main__":
    test_notebook_variables()
