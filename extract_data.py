import csv
import datetime
from bs4 import BeautifulSoup

# Load HTML from file
with open("./content.html", "r") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

dates = []
prices = []
for day in soup.find_all("div", class_="DayPicker-Day"):
    if 'aria-label' in day.attrs:
        date = day.attrs['aria-label']
        price = day.find("p", class_="todayPrice").text.strip()
        dates.append(date)
        prices.append(price)

for date, price in zip(dates, prices):
    print(f"Date: {date}, Price: {price}")
