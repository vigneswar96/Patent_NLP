import pandas as pd
import numpy as np
import os 
import subprocess
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait, as_completed
import csv 
import time 

df = pd.read_csv('E:\\Walsh_work\\Mapping_work\\selected_df.csv')
standards_df= df['Link']
script_path = 'E:\\Walsh_work\\ETSI_Standards.js'
def run_node_script(link, script_path, temp_location):
    command = ['node', script_path, link]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            print(f"Script executed successfully for {link}.")
            return (True, link)
        else:
            print(f"Script failed for {link}. Output: {result.stdout} Errors: {result.stderr}")
            return (False, link)
    except subprocess.TimeoutExpired:
        print(f"Execution timeout for {link}.")
        return (False, link)
    except Exception as e:
        print(f"Execution failed for {link}. Error: {e}")
        return (False, link)
    finally:
        # Attempt cleanup after each run, regardless of success or failure
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

download_location = 'E:\\Walsh_work\\Mapping_work\\ETSI\\'
temp_location = 'C:\\Users\\DELL\\AppData\\Local\\Temp\\'
start_index= 0

successful_downloads = []
failed_downloads = [] 

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(run_node_script, link, script_path, temp_location): link for link in standards_df}
    for future in as_completed(futures):
        success, link = future.result()  # Unpack the result to get success status and link
        if success:
            successful_downloads.append(link)
        else:
            failed_downloads.append(link)

print(f"Successful downloads: {len(successful_downloads)}")
print(f"Failed downloads: {len(failed_downloads)}")
print("Successful links:", successful_downloads)
print("Failed links:", failed_downloads)  