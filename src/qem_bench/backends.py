from qiskit_ibm_runtime.fake_provider import FakeFez

# Returns a backend instance based on the given name. Currently supports only "fake_fez".
# A backend in Qiskit is something that can run circuits
def get_backend(name: str = "fake_fez"):
    if name == "fake_fez":
        return FakeFez()
    raise ValueError(f"Unknown backend: {name}")