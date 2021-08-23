import requests
import json
import redis
import datetime

class Bogbot:
    def __init__(self, word):
        response = requests.get('https://a.4cdn.org/biz/catalog.json')
        self.catalog = json.loads(response.text)
        self.word = word

    def search(self):
        self.urls = []
        for page in self.catalog:
            threads = page['threads']
            for thread in threads:
                no = thread["no"]
                try:
                    sub = thread["sub"]
                    if self.word not in sub:
                        pass
                    else:
                        link = "https://boards.4channel.org/biz/thread/" + str(no)
                        self.urls.append(link)
                except:
                    pass

                try:
                    com = thread["com"]
                    if self.word not in com:
                        pass
                    else:
                        link = "https://boards.4channel.org/biz/thread/" + str(no)
                        self.urls.append(link)
                except:
                    continue

    def store(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        for link in self.urls:
            r.set(link, str(link))

    def email(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        links = [str(r.get(k)) for k in r.keys()]

        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        fromEmail = 'your from email'
        toEmail = 'your to email'
        passw = 'your pword (save as env variable for security)'

        msg = MIMEMultipart('alternative')
        msg['subject'] = 'Ere iz some news on zis market.'
        msg['From'] = fromEmail
        msg['To'] = toEmail

        html = """
            <h4> %s things being discussed u might like: </h4>
            
            %s
            
        """ % (len(links), '<br/><br/>'.join(links))

        mime = MIMEText(html, 'html')
        msg.attach(mime)

        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(fromEmail, passw)
            mail.sendmail(fromEmail, toEmail, msg.as_string())
            mail.quit()
            print('sent')
        except Exception as e:
            print('something went wrong... %s' % e)

        r.flushdb()


#initialize all keywords like this#
keyword = Bogbot('keyword')
keyword.search()
keyword.store()



## email ##
r = redis.Redis(host='localhost', port=6379, db=0)
links = [str(r.get(k)) for k in r.keys()]
if datetime.datetime.now().hour == 13:
    if len(links) > 0:
        keyword.email()
    else:
        pass
