import os
import re
import random
import shutil
from aux_functions import extract_subject_ids, look_for_data_dir

def sample_hcp_subjects(
        source_dir: str,
        output_dir: str,
        n_subjects: int = 10,
        random_seed: int = 42
):
    """
    Randomly samples a specified number of subjects from the HCP dataset
    and copies their relevant files to a new directory.
    
    :param source_dir: path to the full HCP dataset directory
    :param output_dir: path to the directory where sampled files will be copied
    :param n_subjects: number of subjects to sample
    :param random_seed: random seed for reproducibility
    """
    # Set random seed for reproducibility
    random.seed(random_seed)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all subject IDs from .qsdr.fz files
    subject_ids = extract_subject_ids(source_dir)

    # Randomly sample subjects
    sampled_subjects = random.sample(
        subject_ids,
        min(n_subjects, len(subject_ids))
    )

    # Define file extensions to copy for each subject
    extensions_to_copy = [
        ".qsdr.fz",
        ".gqi.fz",
        ".sz",
        "_t1w.nii.gz"
    ]

    copied_files = 0
    # Copy files for each sampled subject
    for sid in sampled_subjects:
        for ext in extensions_to_copy:
            filename = f"{sid}{ext}"
            src = os.path.join(source_dir, filename)

            if os.path.exists(src):
                dst = os.path.join(output_dir, filename)
                shutil.copy2(src, dst)
                copied_files += 1
                print(f"Copied: {filename}")

    # Summary
    print("\n-----------------------------------")
    print(f"Finished.")
    print(f"Subjects sampled: {len(sampled_subjects)}")
    print(f"Files copied: {copied_files}")
    print(f"Output directory: {output_dir}")
    print("-----------------------------------")

if __name__ == "__main__":
    SOURCE_DIR = None # e.g., "/path/to/your/data/directory" 
    if SOURCE_DIR is None: 
        SOURCE_DIR = look_for_data_dir()
    OUTPUT_DIR = f"{SOURCE_DIR}/data_sampled"
    N_SUBJECTS = 10

    sample_hcp_subjects(
        source_dir=SOURCE_DIR,
        output_dir=OUTPUT_DIR,
        n_subjects=N_SUBJECTS
    )