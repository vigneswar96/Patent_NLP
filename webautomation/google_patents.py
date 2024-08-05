import pandas as pd
import numpy as np
import os 
import subprocess
import tempfile
import shutil
import re
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED

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
searchable_gp = np.concatenate((unique_application_number_1,unique_application_number_2))
folder_path = 'E:\\Walsh_work\\Google_patent_Downloads\\1)Patent_pdf'

# Get a list of all files in the folder
present_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
present_files = [name.split('.')[0] for name in present_files]
# Function to extract the main patent number using regular expression
def extract_patent_number(name):
    match = re.search(r'^(US\d+)', name)
    if match:
        return match.group(1)
    else:
        return name
# Create a set of extracted patent numbers from present_files
present_patent_numbers = {extract_patent_number(file) for file in present_files}
# Find the files that need to be downloaded
# files_to_download = [name for name in searchable_gp if name not in present_files]
def check_number_exists(number):
    for present_number in present_patent_numbers:
        if number.startswith(present_number):
            return True
    return False

# Find the files that need to be downloaded
files_to_download = []
for name in searchable_gp:
    if not check_number_exists(name):
        files_to_download.append(name)
os.chdir('E:\\Walsh_work')

def download_patent(patent, tempdir, download_location):
    # Construct the download path
    download_path = os.path.join(download_location, f"{patent}.pdf")

    # Command to run the Node.js script
    command = ['node', 'Google_patents.js', patent]

    # Run the command and capture output
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Successfully downloaded: {patent}")
            return True
        else:
            print(f"Failed to download: {patent}")
            return False
    except subprocess.TimeoutExpired:
        print(f"Timeout expired for {patent}. Node.js script execution took too long.")
        return False
    finally:
        cleanup_temp_folders(tempdir)
def run_node_script(patent, tempdir, download_location):
    # Construct the download path
    download_path = os.path.join(download_location, f"{patent}.pdf")

    # Command to run the Node.js script
    command = ['node', 'Google_patents.js', patent]

    # Run the command and capture output
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        print(f"Timeout expired for {patent}. Node.js script execution took too long.")
        return False
    finally:
        cleanup_temp_folders(tempdir)

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
download_location = 'E:\\Walsh_work\\Google_patent_Downloads\\1)Patent_pdf\\'
temp_location = 'C:\\Users\\DELL\\AppData\\Local\\Temp\\'

successful_downloads = []
failed_downloads = [] 

for patent in files_to_download:
    success = download_patent(patent, temp_location, download_location)
    if success:
        successful_downloads.append(patent)
    else:
        failed_downloads.append(patent)

# Use ThreadPoolExecutor to parallelize the execution
#with ThreadPoolExecutor(max_workers=2) as executor:
 #   pats_to_download = files_to_download
  #  for i in range(0, len(pats_to_download), batch_size):
  #      batch = pats_to_download[i:i + batch_size]
  #      futures = [executor.submit(run_node_script, patent, temp_location, download_location) for patent in batch]
  #      print(f"Submitting batch of {len(batch)} patent numbers:")
  #      for future, patent in zip(futures, batch):
  #          print(f"Submitted: {patent}")
    #futures = [executor.submit(run_node_script, patent, temp_location,download_location) for patent in pats_to_download]
   # print("Submitting patent numbers to the executor:")
   # for future, patent in zip(futures, pats_to_download):
  #      print(f"Submitted:{patent}")
 #   completed_futures, pending_futures = wait(futures, timeout=None, return_when=ALL_COMPLETED)
  #  for future in as_completed_futures:
  #      try:
    #        success = future.result()
      #      if success:
      #          successful_downloads.append(success)
     #       else:
    #            failed_downloads.append(success)
      #  except Exception as e:
   #         print(f"Error: {e}")

 #   for future in pending_futures:
#        print(f"Warning: Future {future} did not complete within the specified timeout.")

#print(f"Successful downloads: {len(successful_downloads)}")
#print(f"Failed downloads: {len(failed_downloads)}")
#print("Successful patents:", [future.result() for future in successful_downloads])
#print("Failed patents:", [future.result() for future in failed_downloads])