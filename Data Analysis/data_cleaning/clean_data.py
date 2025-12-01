#!/usr/bin/env python3
"""
Simple script to combine and clean water level data for linear regression modeling.
Removes preliminary data and cleans missing values.
"""

import csv
import os
from datetime import datetime

def process_folder(folder_name, output_filename):
    """Combine and clean water level CSV files from a specific folder."""
    
    # Create output folder
    os.makedirs("output", exist_ok=True)
    
    # Find all water level CSV files
    csv_files = []
    if not os.path.exists(folder_name):
        print(f"Warning: Folder '{folder_name}' not found!")
        return None
    
    for file in os.listdir(folder_name):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(folder_name, file))
    
    csv_files.sort()  # Sort by year
    
    if not csv_files:
        print(f"No CSV files found in '{folder_name}' folder!")
        return None
    
    print(f"\nFound {len(csv_files)} water level files in '{folder_name}'")
    
    # Prepare output file
    output_file = f"output/{output_filename}"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Write header (only verified data)
        writer.writerow(["Date", "Time", "Verified_ft"])
        
        total_rows = 0
        
        for csv_file in csv_files:
            # Extract year from filename (handle both formats: YYYY.csv or YYYY_*.csv)
            filename = os.path.basename(csv_file)
            year = filename.split('_')[0].replace('.csv', '')
            print(f"Processing {year}...")
            
            with open(csv_file, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)  # Skip header
                
                for row in reader:
                    # Skip rows with missing verified data
                    if len(row) >= 5 and row[4] != "-" and row[4].strip():
                        # Write: Date, Time, Verified
                        writer.writerow([row[0], row[1], row[4]])
                        total_rows += 1
    
    print(f"Cleaned data saved to: {output_file}")
    print(f"Total clean records: {total_rows:,}")
    
    return output_file

def clean_and_combine_data():
    """Combine and clean water level CSV files for ML modeling.
    Automatically discovers and processes all folders containing CSV files."""
    
    # Folders to skip (not data folders)
    skip_folders = {"output", "__pycache__", ".git"}
    
    # Find all folders that contain CSV files
    folders_to_process = []
    
    for item in os.listdir("."):
        if os.path.isdir(item) and item not in skip_folders:
            # Check if folder contains CSV files
            csv_count = sum(1 for f in os.listdir(item) if f.endswith(".csv"))
            if csv_count > 0:
                folders_to_process.append(item)
    
    if not folders_to_process:
        print("No folders with CSV files found!")
        return
    
    print(f"Found {len(folders_to_process)} folder(s) with CSV files to process")
    print("=" * 40)
    
    # Process each folder
    for folder_name in sorted(folders_to_process):
        # Generate output filename: cleaned_<folder_name_lowercase_with_underscores>_water_levels.csv
        output_name = folder_name.lower().replace(" ", "_").replace("-", "_")
        output_filename = f"cleaned_{output_name}_water_levels.csv"
        process_folder(folder_name, output_filename)

if __name__ == "__main__":
    print("Water Level Data Cleaner")
    print("=" * 40)
    clean_and_combine_data()
    print("\nDone!")
