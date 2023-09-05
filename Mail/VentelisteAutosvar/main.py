# Receive mails
import imaplib
from email import policy
from email.parser import BytesParser

# Send mails
import smtplib
from email.mime.text import MIMEText

## Step 1: Reading Emails with imaplib
# Connect to the IMAP server
server = imaplib.IMAP4_SSL('imap.gmail.com')

# Login to your account
server.login('your_email@gmail.com', 'your_password')

# Select the inbox
server.select('inbox')

# Search for emails
result, data = server.search(None, 'ALL')

# Fetch and read emails
email_ids = data[0].split()
for email_id in email_ids:
    result, email_data = server.fetch(email_id, '(RFC822)')
    msg = BytesParser(policy=policy.default).parsebytes(email_data[0][1])
    print('Subject:', msg['subject'])
    print('From:', msg['from'])
    print('Body:', msg.get_body().get_payload(decode=True))

# Step 2: Sending Emails with smtplib

msg = MIMEText('This is the body of the email')
msg['Subject'] = 'Subject of the Email'
msg['From'] = 'your_email@gmail.com'
msg['To'] = 'recipient_email@gmail.com'

# Connect to the SMTP server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

# Login to your account
server.login('your_email@gmail.com', 'your_password')

# Send the email
server.sendmail('your_email@gmail.com', 'recipient_email@gmail.com', msg.as_string())

# Close the connection
server.quit()