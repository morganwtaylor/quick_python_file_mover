import os
import shutil
import zipfile
import hashlib

# specify the source and destination directories
source_dir = './Files/'
dest_dir = './Moved/'
zip_file = 'csv_files.zip'
log_file = 'csv_files_log.txt'

# Iterate over all files and subdirectories in source directory
csv_files = []
with open(log_file, 'w') as f:
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
             # Get the latest file in each subdirectory
            latest_file = max(os.listdir(os.path.join(dirpath, dirname)), key=lambda x: os.path.getmtime(os.path.join(dirpath, dirname, x)))
            # Check if file is a csv
            if latest_file.endswith('.txt'):
                # Construct full filepaths
                source_file = os.path.join(dirpath, filename)
                csv_files.append(source_file)
                # Get the file size and write to log file
                file_size = os.path.getsize(source_file)
                f.write(f'File: {source_file}, Size: {file_size} bytes\n')
    with zipfile.ZipFile(zip_file, 'w') as myzip:
        for file in csv_files:
            myzip.write(file)
    # Get the hash of the zip file before moving
    sha256_hash = hashlib.sha256()
    with open(zip_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

with open(log_file,'a') as f:
    f.write(f'Hash of the zip file: {sha256_hash.hexdigest()}\n')

# Move the zip file 
shutil.move(zip_file, dest_dir)
# Get the hash of the zip file after moving
zip_file_path = os.path.join(dest_dir, zip_file)
sha256_hash_after = hashlib.sha256()
with open(zip_file_path, "rb") as f:
    for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash_after.update(byte_block)
    #open the log file in append mode
    with open(log_file,'a') as f:
        f.write(f'Hash of the zip file after moving: {sha256_hash_after.hexdigest()}\n')
print("All .csv files have been zipped and moved to", dest_dir)
print("Log file has been created at ", log_file)
