import os
import re
import random
import pandas as pd
from aux_functions import extract_subject_ids, look_for_data_dir
# set random seed for reproducibility
random.seed(42)

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

        # Create fake gender values
        sex = random.choice(["M", "F"])

        # Create fake school values ranging from 0 to 10
        school = random.randint(0, 10)

        # Create fake physical activity values ranging from 1 to 5
        physical = random.randint(1, 5)

        # Create fake tobacco usage values (0 or 1)
        tobacco = random.randint(0, 1)

        # Create fake income values ranging from 0 to 9
        income = random.randint(0, 9)

        rows.append({
            "subject_id": sid,
            "bmi": bmi,
            "age": age,
            "sex": sex,
            "school": school,
            "physical": physical,
            "tobacco": tobacco,
            "income": income})

    # synthesize the data into a DataFrame
    df = pd.DataFrame(rows)
    output_csv = os.path.join(data_dir, output_name)

    df.to_csv(output_csv, index=False)

    print(f"Saved CSV to:\n{output_csv}")

if __name__ == "__main__":
    # Update this to your actual data directory
    data_dir = None # e.g., "/path/to/your/data/directory" 
    if data_dir is None: 
        data_dir = look_for_data_dir()
        
    create_fake_demographic_data(data_dir)
