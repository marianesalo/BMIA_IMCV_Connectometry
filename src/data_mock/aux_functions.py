import re
import os

def extract_subject_ids(data_dir: str) -> list:
    """
    Extracts subject IDs from .qsdr.fz filenames in the specified directory.
    
    :param data_dir: path to the directory containing the .qsdr.fz files
    :return: a sorted list of unique subject IDs
    """
    # list all files in the directory
    files = os.listdir(data_dir)
    print(f"Found {len(files)} files in the directory.")

    # extract subject IDs from the filenames
    subject_ids = []

    for f in files:
        if f.endswith(".qsdr.fz"):
            match = re.match(r"(\d+)\.qsdr\.fz", f)
            if match:
                subject_ids.append(match.group(1))

    # Remove duplicates and sort
    subject_ids = sorted(list(set(subject_ids)))
    print(f"Found {len(subject_ids)} subjects")
    
    return subject_ids

def look_for_data_dir() -> str:
    """Tries to find the data directory in the current working directory."""
    print("Trying to fetch source dir from the cwd...")
    print("Assuming there is a 'data' directory with the .qsdr.fz files in the current working directory.")
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, "data")
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")
    return data_dir