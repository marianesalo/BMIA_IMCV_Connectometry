import os
import re
import random
import pandas as pd
# set random seed for reproducibility
random.seed(42)

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



def create_fake_demographic_data(
        data_dir: str,
        output_name: str = "fake_demographics.csv"
):
    """
    Creates a fake demographic dataset for HCP subjects 
    based on the name of the .qsdr.fz files in the specified directory.
    
    :param data_dir: path to the directory containing the .qsdr.fz files
    :param output_name: name of the output CSV file
    :return: a pandas DataFrame with the fake demographic data
    """
    subject_ids = extract_subject_ids(data_dir)

    rows = []

    for sid in subject_ids:
        # Create fake BMI values ranging from 18 to 40
        bmi = round(random.uniform(18.0, 40.0), 1)
        # Create fake age values ranging from 22 to 37
        age = random.randint(22, 37)

        rows.append({"subject_id": sid, "bmi": bmi, "age": age})

    # synthesize the data into a DataFrame
    df = pd.DataFrame(rows)
    output_csv = os.path.join(data_dir, output_name)

    df.to_csv(output_csv, index=False)

    print(f"Saved CSV to:\n{output_csv}")

if __name__ == "__main__":
    # Update this to your actual data directory
    data_dir = None # e.g., "/path/to/your/data/directory" 
    if data_dir is None: 
        print("Trying to fetch data dir from the cwd...")
        print("Assuming there is a 'data' directory with the .qsdr.fz files in the current working directory.")
        cwd = os.getcwd()
        data_dir = os.path.join(cwd, "data")
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Data directory not found at: {data_dir}")
        
    create_fake_demographic_data(data_dir)