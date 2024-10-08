import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
import json


def send(subject, body, attachment_path=None):
    # JSONファイルを読み込む
    with open('config.json', 'r') as f:
        config = json.load(f)

    from_address = config['from_address']
    to_address = config['to_address']
    password = config['password']

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Date'] = formatdate(localtime=True)

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 添付ファイルの追加
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={attachment_path.split("/")[-1]}',
            )
            msg.attach(part)

    # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(from_address, password)
    # 作成したメールを送信
    smtpobj.sendmail(from_address, to_address, msg.as_string())
    smtpobj.close()

