import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

MAIN_DIR = "flight_prices"

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        data = list(reader)
    return data

def analyze_data(group):
    group_dir = os.path.join(MAIN_DIR, group)
    files = sorted([f for f in os.listdir(group_dir) if f.endswith('.csv')])
    
    all_data = {}
    for file in files:
        filepath = os.path.join(group_dir, file)
        data = read_csv(filepath)
        all_data[file] = data
        
    return all_data

def convert_date_format(date_str):
    # Convert the date string into a datetime object
    dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # Return the date in the desired format
    return dt_obj.strftime('%b %d')

def plot_data(all_data, group):
    plt.figure(figsize=(15,8))
    
    for file, data in all_data.items():
        dates = [convert_date_format(row[0]) for row in data]
        prices = [int(row[1]) for row in data]
        plt.plot(dates, prices, marker='o', label=file)
        
    plt.title(f"Price Analysis for {group}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

print("Available groups:")
groups = [d for d in os.listdir(MAIN_DIR) if os.path.isdir(os.path.join(MAIN_DIR, d))]
for idx, grp in enumerate(groups, 1):
    print(f"{idx}. {grp}")

try:
    choice_idx = int(input("Choose a group number to analyze: "))
    if choice_idx <= 0:
        raise IndexError
    chosen_group = groups[choice_idx - 1]  # since index starts at 0

    all_data = analyze_data(chosen_group)
    plot_data(all_data, chosen_group)
except (ValueError, IndexError):
    print("Invalid choice.")





