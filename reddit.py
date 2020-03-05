#! python3
import os
import praw
import pandas as pd
import datetime as dt
import smtplib, ssl

# import the corresponding modules
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Environment Variables.
ra_user = os.environ.get("RA_User")
ra_password = os.environ.get("RA_Password")
praw_client_id = os.environ.get("RA_Client_Id")
praw_client_secret = os.environ.get("RA_Client_Secret")
praw_user_agent = os.environ.get("RA_User_Agent")



# Authorized Reddit Instance.
reddit = praw.Reddit(client_id = praw_client_id,
                     client_secret = praw_client_secret,
                     user_agent = praw_user_agent,
                     )


print(reddit.read_only)
reddit.read_only = True

#print(reddit.user.me())


# Obtaining a Subreddit Instance.
subreddit = reddit.subreddit("OnePiece")

print(subreddit.display_name)
#print(subreddit.title)
#print(subreddit.description)


# Submission Instances.
for submission in reddit.subreddit("OnePiece").hot(limit = 10):
    print(submission.title)
    print("-------------")
    print(submission.score,
          submission.id,
          submission.url
          )


# WORK ON SCRAPING AND SAVING/LOADING SCRAPED DATA IN JSON FORMAT SOON!
# March 1, 2020 Work Continues.


op_dict = {
    "Title": [], \
    "Score": [], \
    "Id": [], \
    "Url": [], \
    "Created": [], \
    }

for submission in reddit.subreddit("OnePiece").hot(limit = 10):
    op_dict["Title"].append(submission.title)
    op_dict["Score"].append(submission.score)
    op_dict["Id"].append(submission.id)
    op_dict["Url"].append(submission.url)
    op_dict["Created"].append(submission.created)

op_data = pd.DataFrame(op_dict)

def date(created):
    return dt.datetime.fromtimestamp(created)

Time_stamp = op_data["Created"].apply(date)

op_data = op_data.assign(timestamp = Time_stamp)

op_data.to_csv("ONEPIECE SCRAPES.csv", index = False)


# Emails parsed data with csv file attachment.

SUBJECT = 'Daily Reddit Scrape'
FILENAME = 'ONEPIECE SCRAPES.csv'
FILEPATH = './ONEPIECE SCRAPES.csv'
MY_EMAIL =
MY_PASSWORD =
TO_EMAIL = 'louieviray017@yahoo.com'
SMTP_SERVER = 'Smtp.mail.yahoo.com'
SMTP_PORT = 465

msg = MIMEMultipart()
msg['From'] = MY_EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = SUBJECT

part = MIMEBase('application', "octet-stream")
part.set_payload(open(FILEPATH, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=FILENAME)  # or
# part.add_header('Content-Disposition', 'attachment; filename="attachthisfile.csv"')
msg.attach(part)

smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(MY_EMAIL, MY_PASSWORD)
smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
smtpObj.quit()

# Email CSV File to recipient function does not work.