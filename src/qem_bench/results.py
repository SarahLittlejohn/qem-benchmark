"""Handles storing the benchmark results."""
"""Save and load benchmark results, one row per run."""

# represents file and folder paths as objects, which is neater than joining strings
from pathlib import Path

# Pandas is the standard Python library for tables of data
import pandas as pd

# The directory where all result CSV files will be stored
RESULTS_DIR = Path("results")

# Takes a list of dictionaries (one per run) and a name for the file, and returns the path it saved to.
def save(rows: list[dict], name: str) -> Path:
    # Creates the results/ folder. exist_ok=True means it won't error if the folder's already there.
    RESULTS_DIR.mkdir(exist_ok=True)
    # Construct the full path to the CSV file for this benchmark name.
    path = RESULTS_DIR / f"{name}.csv"

    # Turns your list of dictionaries into a table, with each dictionary becoming a row and each key a column.
    # Append to the end of the file rather than overwriting it.
    # Writes the column names only if the file is new, so they don't get repeated every time you append.
    pd.DataFrame(rows).to_csv(path, mode="a", header=not path.exists(), index=False)
    return path

# Loads the results for a given benchmark name as a Pandas DataFrame.
def load(name: str) -> pd.DataFrame:
    """Load results/<name>.csv as a table."""
    return pd.read_csv(RESULTS_DIR / f"{name}.csv")