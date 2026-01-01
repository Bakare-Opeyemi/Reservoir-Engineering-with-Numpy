# Reservoir Engineering with NumPy

**Project:** Reservoir Material Balance Analysis (Havlena–Odeh method)

This repository demonstrates a material-balance based analysis for reservoir engineering using NumPy, SciPy and pandas. The notebooks implement corrections to gas/oil PVT calculations, the Havlena–Odeh straight-line method, and a simple performance prediction routine. The package also includes automated tests that execute the main notebook and validate key variables.

**Contents**
- `final_notebook.ipynb`: Final, corrected Jupyter notebook that performs the material balance analysis, Havlena–Odeh regression, and a simple performance prediction for cumulative production. This notebook contains the working code and prints key results such as `Bg_corrected`, `F_havlena`, `Eo_havlena`, `original_oil_in_place`, and `Np_predicted`.
- `initial_notebook.ipynb`: Initial/noted version highlighting issues and earlier (incorrect) implementations; useful for comparison and teaching.
- `test_notebook.py`: Pytest script that executes `final_notebook.ipynb` and performs assertions on computed arrays and variables to ensure correctness.

**Key concepts implemented**
- Corrected gas formation volume factor (`Bg_corrected`) calculation using standard conditions.
- Havlena–Odeh straight-line method (F vs Eo) for estimating original oil in place (OOIP).
- Material balance equation including water influx (`We` and `Bw`) and a simple treatment of gas terms.
- A basic performance prediction solving for predicted cumulative oil production `Np_predicted` at different pressures.

Project highlights for readers and reviewers:
- The `final_notebook.ipynb` defines and prints these key variables that the tests validate: `Bg_corrected`, `F_havlena`, `Eo_havlena`, `F_material_balance`, `Np_predicted`, `original_oil_in_place`, and `gas_cap_ratio`.

Getting started
---------------

Prerequisites
- Python 3.8+ recommended
- The notebooks and tests rely on these Python packages: `numpy`, `pandas`, `scipy`, `nbformat`, `nbconvert`, and `pytest`.

Install dependencies (recommended in a virtual environment)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy pandas scipy nbformat nbconvert pytest
```

Running the notebooks
- To open and interact with the notebooks:

```bash
jupyter lab    # or `jupyter notebook`
```

- To execute `final_notebook.ipynb` from the command line (headless):

```bash
jupyter nbconvert --to notebook --execute final_notebook.ipynb --ExecutePreprocessor.timeout=600 --output executed_final_notebook.ipynb
```

Running tests
-------------
- The repository includes `test_notebook.py` which:
  - Executes `final_notebook.ipynb` and checks for successful execution.
  - Imports variables from the executed notebook and validates numerical results and shapes.

- Run the tests with:

```bash
pytest -q
```

Notes about the tests
- The tests expect `final_notebook.ipynb` to define `Bg_corrected` (array of 5 positive values), `F_havlena`, `Eo_havlena`, `F_material_balance`, `Np_predicted` (array length 5 with initial element 0), `original_oil_in_place` and `gas_cap_ratio`.
- Tolerances in tests are set to allow small numerical differences due to floating point arithmetic.

Design and pedagogy
-------------------
- `initial_notebook.ipynb` documents the original mistakes and serves as a teaching aid to compare incorrect and corrected implementations (for example, incorrect `Bg` formula and omitted Havlena–Odeh implementation).
- `final_notebook.ipynb` contains a cleaned-up, corrected analysis intended to be reproducible and testable with `pytest`.

Suggested next steps / improvements
- Add a `requirements.txt` or `pyproject.toml` for reproducible installs.
- Add more robust uncertainty quantification on regression results and sensitivity tests for input PVT correlations.
- Add a small CLI script to run the analysis non-interactively and produce CSV/plots of predicted vs actual production.

License & attribution
- No license file is included. If you plan to share or publish, consider adding an appropriate open-source license (e.g., MIT, Apache-2.0) and attribution.

Contact / Maintainer
- If you (the repository owner) want, add maintainer contact info here.

Acknowledgements
- This project is a compact educational demonstration of material balance methods in reservoir engineering implemented in a Python notebook.

---
Generated from repository notebooks on: Jan 1, 2026
