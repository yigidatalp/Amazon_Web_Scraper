# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 12:13:52 2023

@author: Yigitalp
"""

# Import libraries
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime
import csv
import pandas as pd

#%%
#################### Run this one-time until the method
# Connect to website
url = 'https://www.amazon.com/N-Analyst-Scientist-Programmer-Statistics/dp/B091Q331DS/ref=sr_1_2?crid=2LVHYAPJXGG74&keywords=data+analyst+shirt&qid=1689332774&sprefix=data+analyst+shir%2Caps%2C174&sr=8-2'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

page = requests.get(url, headers=headers)

soup1 = BeautifulSoup(page.content, 'html.parser')

soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

# Extract product title
try:
    product_title = soup2.find(
        id='productTitle').get_text().strip().split(',')[1].strip()
except AttributeError:
    product_title = ''

# Extract product price
try:
    product_price = float(soup2.find(
        id='corePrice_desktop').get_text().strip().split()[1][1:])
except AttributeError:
    product_price = ''

# Extract today's date
today = datetime.date.today()

# Create header and data lists
header = ['Product', 'Price', 'Date']
data = [product_title, product_price, today]

# Append the next data rows
with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(data)
#################### Run this one-time until the method
#%%

# Method for data appending to .csv file


def check_price():
    # Connect to website
    url = 'https://www.amazon.com/N-Analyst-Scientist-Programmer-Statistics/dp/B091Q331DS/ref=sr_1_2?crid=2LVHYAPJXGG74&keywords=data+analyst+shirt&qid=1689332774&sprefix=data+analyst+shir%2Caps%2C174&sr=8-2'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    page = requests.get(url, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')

    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    # Extract product title
    try:
        product_title = soup2.find(
            id='productTitle').get_text().strip().split(',')[1].strip()
    except AttributeError:
        product_title = ''

    # Extract product price
    try:
        product_price = float(soup2.find(
            id='corePrice_desktop').get_text().strip().split()[1][1:])
    except AttributeError:
        product_price = ''

    # Extract today's date
    today = datetime.date.today()

    # Create header and data lists
    # header = ['Product', 'Price', 'Date']
    data = [product_title, product_price, today]

    # Append the next data rows
    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)


# Set time for while loop
timeout = 10  # 24*60*60 day
timeout_start = time.time()
while time.time() <= timeout_start + timeout:
    check_price()

# Read in the .csv file to check/control
df = pd.read_csv('AmazonWebScraperDataset.csv')
df = df.dropna()

# Method for e-mail sending


def send_email():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    # server.starttls()
    server.ehlo()
    email_address = 'yigitalpozmen@gmail.com'
    server.login(email_address, '**************')
    subject = 'The t-shirt you want is below $15! Now is your chance to buy!'
    body = f"Yigitalp, This is the moment we have been waiting for. Now is your chance to pick up the shirt of your dreams. Don't mess it up! Link here: {url}"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(email_address, msg)


# Check if price condition is met, if true then send an e-mail
for price in df['Price']:
    if price <= 15:
        send_email()
