import requests # http requests
from bs4 import BeautifulSoup #web scarping
import smtplib #send email
#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#system date time manupulation
import datetime
now=datetime.datetime.now()
#email conetent placeholder
content=''

#extracting the Hacker news stories

def extract_news(url):
    print("extracting hacker news stories...")
    cnt=''      #temporary placeholder
    cnt+=('<b>HN Top Series:</b>\n'+'<br>'+'-'*50+'br')
    response=requests.get(url) #getting response from url and stored into requests objcet
    content=response.content#To see the response’s content in bytes, you use .content
    soup=BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':' '})):
        cnt+=((str(i+1)+'::'+tag.text +"\n"+'<br>') if tag.text!='More' else '')
    return (cnt)

cnt=extract_news('https://news.ycombinator.com')
content+=cnt
content+=('<br>--------<br>')
content+=('<br><br> End of Message')


#composing email

SERVER='smtp.gmail.com'#smtp server
PORT=587#your port number
FROM='iicsinhgad@gmail.com'
TO='pratikgade5151@gmail.com'
PASS='******'

msg=MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()

