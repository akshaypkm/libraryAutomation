import csv
from datetime import datetime, timedelta
import pandas as pd
import os
import time

# Dictionary to store the last entry time for each roll number
last_entry_times = {}

def file_exists(file_path):
    return os.path.exists(file_path)

def log_entry(roll_number, filename):
    global last_entry_times
    
    # Get current date and time
    entry_date = datetime.now().strftime('%Y-%m-%d')
    entry_time = datetime.now().strftime('%H:%M:%S')

    # Check if roll number exists in the last_entry_times dictionary and if the last entry time is within 30 seconds
    if roll_number in last_entry_times and datetime.now() - last_entry_times[roll_number] < timedelta(seconds=30):
        print("Entry skipped. Please wait 30 seconds before logging again.")
        return

    # Update the last entry time for the roll number
    last_entry_times[roll_number] = datetime.now()

    # Read the existing CSV file
    if file_exists(filename):
        with open(filename, mode='r', newline='') as file:
            csvFile = csv.reader(file)
            data = list(csvFile)
            for row in data:
                if row[2] == str(roll_number) and row[5] == "":  # Check if roll number exists and exit time is not recorded
                    row[5] = entry_time  # Update exit time of previous entry
                    with open(filename, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                    return  # Exit the function after updating exit time

    # Read the existing XLSX file
    df = pd.read_excel('sampleData.xlsx')

    # Check if the roll number column exists
    if 'Roll_no' in df.columns:
        # Search for the roll number in the DataFrame
        matched_row = df.loc[df['Roll_no'] == roll_number]

        if not matched_row.empty:
            # Get the name corresponding to the matched roll number
            name = matched_row.iloc[0]['Name']
            
            # Check if CSV file exists
            if file_exists(filename):
                with open(filename, mode='r', newline='') as file:
                    csvFile = csv.reader(file)
                    count = sum(1 for _ in csvFile)

                with open(filename,'a',newline='') as file:
                    writer = csv.writer(file)
                    if os.stat(filename).st_size == 0:
                        writer.writerow(["S.No", "Name", "Roll Number", "Date", "Entry Time", "Exit Time"])  # Writing headers
                    # Write the entry details to the CSV file
                    writer.writerow([count, name, roll_number, entry_date, entry_time, ""])  # Exit time initially empty
                
            else:
                with open(filename,'w',newline='') as file:
                    writer = csv.writer(file)
                    b=0
                    if os.stat(filename).st_size == 0:
                        writer.writerow(["S.No", "Name", "Roll Number", "Date", "Entry Time", "Exit Time"])  # Writing headers
                      # Write the entry details to the CSV file
                    writer.writerow([b + 1, name, roll_number, entry_date, entry_time, ""])  # Exit time initially empty
        else:
            print("Roll number not found in the existing data.")
    else:
        print("Column 'roll_no' not found in the existing data.")

def main():
    while True:
        # Ask for the roll number
        roll_number_input = input("Please enter your roll number: ").strip()  # Trim whitespace
        try:
            roll_number = int(roll_number_input)
        except ValueError:
            print("Invalid input. Roll number must be an integer.")
            continue

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f"library_log_{current_date}.csv"

        # Log the entry
        log_entry(roll_number, filename)

        print("Entry logged successfully.")

if __name__ == "__main__":
    main()
