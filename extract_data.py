import os
import csv
from datetime import datetime
from bs4 import BeautifulSoup

MAIN_DIR = "flight_prices"

# Ensure the main directory exists
if not os.path.exists(MAIN_DIR):
    os.makedirs(MAIN_DIR)


def save_data(dates, prices, group):
    # Ensure the main directory exists
    if not os.path.exists(MAIN_DIR):
        os.makedirs(MAIN_DIR)

    group_dir = os.path.join(MAIN_DIR, group)

    # Ensure the group directory exists
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(group_dir, f"{timestamp}.csv")

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Price"])
        writer.writerows(zip(dates, prices))

    print(f"Data saved to {filepath}")


# Load HTML from file
with open("./content.html", "r") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extracting data
dates = []
prices = []

for day in soup.find_all("div", class_="DayPicker-Day"):
    if 'aria-label' in day.attrs:
        date_str = day.attrs['aria-label']
        # Convert date string to Python datetime object
        date_obj = datetime.strptime(date_str, '%a %b %d %Y')
        dates.append(date_obj)

        price_str = day.find("p", class_="todayPrice").text.strip()
        # Extract integer value from the price string
        price = int("".join(filter(str.isdigit, price_str)))
        prices.append(price)

# Choose a group
print("Available groups:")
groups = [d for d in os.listdir(
    MAIN_DIR) if os.path.isdir(os.path.join(MAIN_DIR, d))]
for idx, grp in enumerate(groups, 1):
    print(f"{idx}. {grp}")

choice = int(
    input("Choose a group by number or enter 0 to create a new group: "))

if choice == 0:
    new_group = input("Enter the name for the new group: ")
    os.makedirs(os.path.join(MAIN_DIR, new_group))
    group_path = os.path.join(MAIN_DIR, new_group)
else:
    group_path = os.path.join(MAIN_DIR, groups[choice - 1])


if choice == 0:
    save_data(dates, prices, new_group)
else:
    save_data(dates, prices, groups[choice - 1])