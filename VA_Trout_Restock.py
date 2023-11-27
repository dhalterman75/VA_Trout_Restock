import re
import requests
from datetime import date
import json
import smtplib
from email.message import EmailMessage

# Logs into gmail account using smtp, creates email message and sends to my email account
def send_message(match):
    text = f'{match[2]} in {match[1]} was stocked today.'
    message = EmailMessage()
    message.set_content(text)
    message['subject'] = 'TROUT RESTOCK'
    message['to'] = cfg['RECIPIENT']

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(cfg['SENDER'], cfg['SENDER_PASSWORD'])
    server.send_message(message)
    server.quit()

def send_not_found():
    message = EmailMessage()
    message.set_content('No stockings in your preferred counties today.')
    message['subject'] = 'TROUT RESTOCK'
    message['to'] = cfg['RECIPIENT']

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(cfg['SENDER'], cfg['SENDER_PASSWORD'])
    server.send_message(message)
    server.quit()

# Pulls county list from county_list.txt
county_filename = 'county_list.txt'
county_file = open(county_filename, "r")
counties = county_file.read()

# Pulls config values from config.json
config_filename = 'config.json'
config_file = open(config_filename, "r")
cfg = json.load(config_file)

# Load the VA DWR webpage from url
url = "https://dwr.virginia.gov/fishing/trout-stocking-schedule/"
result = requests.get(url)

# Find the data table of stocked locations
pattern = r'<tr><td class="date_stocked">(.*?)</td><td class="locality_name">(.*?)</td><td class="waterbody_details">(.*?)<'
trim = re.findall(pattern, result.text)

# Find out if a location in one of my desired counties was stocked today
today = date.today().strftime("%B %d, %Y")
found = False
for match in trim:
    if today == match[0] and match[1] in counties:
        send_message(match)
        found = True

if not found:
    send_not_found()