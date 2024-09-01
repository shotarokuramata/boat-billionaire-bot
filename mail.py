import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import json

def send_mail(subject, body):
    # JSONファイルを読み込む
    with open('config.json', 'r') as f:
        config = json.load(f)

    from_address = config['from_address']
    to_address = config['to_address']
    password = config['password']

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Date'] = formatdate(localtime=True)


    # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(from_address, password)
    # 作成したメールを送信
    smtpobj.sendmail(from_address, to_address, msg.as_string())
    smtpobj.close()

