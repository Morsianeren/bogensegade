# Receive mails
import imaplib
from email import policy
from email.parser import BytesParser

# Writing csv file
import re
import csv

with open('login.txt', 'r') as file:
    username = file.readline().strip()
    password = file.readline().strip()

csv_file = open('extracted_emails.csv', 'w', newline='', encoding='UTF-8')
csv_writer = csv.writer(csv_file)
csv_header = ['Dato', 'Navn', 'Mail', 'Foraeldrekoeb', 'Besked']
csv_writer.writerow(csv_header)  # Write the header

## Step 1: Reading Emails with imaplib
# Connect to the IMAP server
server = imaplib.IMAP4_SSL('imap.one.com')

# Login to your account
server.login(username, password)

# Read what kind of labels are available
""" result, folders = server.list()
for folder in folders:
    print(folder) """

# Select the inbox
server.select('INBOX.Venteliste')

# Search for emails
result, data = server.search(None, 'ALL')

# Fetch and read emails
email_ids = data[0].split()
for email_id in email_ids:
    result, email_data = server.fetch(email_id, '(RFC822)')
    msg = BytesParser(policy=policy.default).parsebytes(email_data[0][1])

    # Get the body of the email
    body = msg.get_body().get_payload(decode=True)
    
    # Find all email addresses in the body
    email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(body))
    if len(email_addresses) != 0:
        csv_writer.writerow([email_addresses[0]])

    print('Subject:', msg['subject'])
    print('From:', msg['from'])
    print('Date:', msg['date'])
    print('')
    #print('Body:', msg.get_body().get_payload(decode=True))


csv_file.close()
# server.quit()
