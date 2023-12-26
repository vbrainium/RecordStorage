#!/usr/bin/env python3
# Converts .mov video files to .mp4 format. 
# Sets up logging, input/output directories. 
# Loops through .mov files, converts with HandBrakeCLI, 
# moves original to processed folder, logs info.

import os
import subprocess
import logging
import time

# Setting up logging
log_file = os.path.expanduser("~/Desktop/video_processor.log")
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
desktop_path = os.path.expanduser("~/Desktop")
source_directory = desktop_path
output_directory = os.path.join(desktop_path, "output")
processed_directory = os.path.join(desktop_path, "processed")

# Check and create output and processed directories if they don't exist
os.makedirs(output_directory, exist_ok=True)
os.makedirs(processed_directory, exist_ok=True)

logging.info("Script started.")

mov_files = [file for file in os.listdir(source_directory) if file.endswith(".mov")]

if not mov_files:
    logging.info("No .mov files found for processing. Exiting.")
    exit()

start_time = time.time()

for file in mov_files:
    input_file = os.path.join(source_directory, file)
    output_file = os.path.join(output_directory, file.replace(".mov", ".mp4"))
    initial_size = os.path.getsize(input_file) / (1024 * 1024)  # in MB

    logging.info(f"Processing file: {file}")

    # Convert using HandBrakeCLI
    try:
        subprocess.run(["/usr/local/bin/HandBrakeCLI", "-i", input_file, "-o", output_file, "--preset=Fast 1080p30"], check=True)
        logging.info(f"Conversion successful: {file} to {output_file}")

        final_size = os.path.getsize(output_file) / (1024 * 1024)  # in MB

        # Move the original mov file to the processed directory
        os.rename(input_file, os.path.join(processed_directory, file))
        logging.info(f"Moved original file to processed directory: {file}")

        logging.info(f"File: {file}, Initial Size: {initial_size:.2f} MB, Final Size: {final_size:.2f} MB")
    except subprocess.CalledProcessError:
        logging.error(f"Error during conversion: {file}")
    except Exception as e:
        logging.error(f"Unexpected error for file {file}: {str(e)}")

duration = time.time() - start_time
logging.info(f"Script finished. Total duration: {duration:.2f} seconds.")

