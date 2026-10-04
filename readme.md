## To do

### Setup
- [x] Project structure, `pyproject.toml` and virtual environment
- [x] GitHub repo
- [x] IBM Quantum account and saved credentials

### 4 Oct: GHZ circuit
- [x] GHZ circuit module (`circuits/ghz.py`)
- [x] Noiseless test for GHZ (`tests/test_circuits.py`)

### 10–11 Oct: Baseline on a noisy simulator
- [x] Baseline technique with no mitigation (`mitigation/none.py`)
- [ ] Runner and results saving (`runner.py`, `results.py`)
- [ ] First chart: raw GHZ value against number of qubits
- [ ] Mirror circuit module and test

### 17–18 Oct: Mitigation techniques
- [ ] Ising circuit module and test
- [ ] Readout error mitigation (mthree)
- [ ] Zero-noise extrapolation (Mitiq)
- [ ] Dynamical decoupling
- [ ] YAML configs for experiments
- [ ] Stretch: probabilistic error cancellation (Mitiq)

### 24–25 Oct: Real hardware
- [ ] Choose the most interesting configurations from simulator results
- [ ] Run on IBM hardware with my own mitigation
- [ ] Run the same on hardware with Runtime's built-in mitigation for comparison

### 31 Oct: Analysis and write-up
- [ ] Analysis notebook and charts
- [ ] Write up findings in this README