import pandas as pd
import numpy as np
import os 
import subprocess
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

df = pd.read_csv(r'E:\Walsh_work\DynamicReport_2023-12-08_173218.csv',low_memory=False,skiprows=16)
df_new = df.dropna(subset=['ETSI Projects','Publication Numbers'],how='any')
filtered_df= df_new[df_new['ETSI Projects']!='-']
unique_publication_numbers=filtered_df['Publication Numbers'].unique()
# Assuming 'Publication Numbers' contains strings with a '|' separator
result = filtered_df['Publication Numbers'].str.partition('|', expand=True)

# Select the first and third columns
application_publication_number_1 = result[0]
application_publication_number_2 = result[2]
unique_application_number_1=application_publication_number_1.unique()
unique_application_number_2=application_publication_number_2.unique()
result= np.concatenate((unique_application_number_1,unique_application_number_2))
searchable_gp=result
os.chdir('E:\\Walsh_work')
def run_node_script(patent, tempdir, download_location):
    # Construct the download path
    download_path = os.path.join(download_location, f"{patent}.pdf")

    # Command to run the Node.js script
    command = ['node', 'Google_patents.js', patent]

    # Run the command and capture output
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        
    except subprocess.TimeoutExpired:
        print(f"Timeout expired for {patent}. Node.js script execution took too long.")
    finally:

        cleanup_temp_folders(temp_location)
def cleanup_temp_folders(temp_location):
    try:
        # List all files and subdirectories in the specified location
        entries = os.listdir(temp_location)

        # Iterate over each entry
        for entry in entries:
            entry_path = os.path.join(temp_location, entry)

            # Check if the entry is a directory
            if os.path.isdir(entry_path):
                # Remove the directory and its contents
                remove_directory(entry_path)

    except Exception as e:
        print(f"Error cleaning up temp folders: {e}")

def remove_directory(directory_path):
    try:
        # Remove the directory and its contents
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)

        # Remove the top-level directory
        os.rmdir(directory_path)

    except Exception as e:
        print(f"Error removing directory: {e}")
# Set the download location and temporary directory
download_location = 'E:\\Walsh_work\\Google_patent_Downloads\\Patent_pdf\\'
temp_location = 'C:\\Users\\DELL\\AppData\\Local\\Temp\\'

successful_downloads = []
failed_downloads = [] 

start_index=100500
# Use ThreadPoolExecutor to parallelize the execution
with ThreadPoolExecutor(max_workers=15) as executor:
    patents_to_download = searchable_gp[start_index:]
    futures = [executor.submit(run_node_script, patent, temp_location,download_location) for patent in patents_to_download]
    
    completed_futures, pending_futures = wait(futures, timeout=None, return_when=ALL_COMPLETED)
    for future in completed_futures:
        try:
            success=future.result()
            if success:
                successful_downloads.append(success)
            else:
                failed_downloads.append(success)
        except Exception as e:
            print(f"Error: {e}")

    for future in pending_futures:
        print(f"Warning: Future {future} did not complete within the specified timeout.")
        
print(f"Successful downloads: {len(successful_downloads)}")
print(f"Failed downloads: {len(failed_downloads)}")
print("Successful patents:", [future.result() for future in successful_downloads])
print("Failed patents:", [future.result() for future in failed_downloads])