from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import smtplib
import threading


class EmailHelper:
    def __init__(self, from_addr, password, to_addr, smtp_server):
        self.from_addr = from_addr
        self.password = password
        self.to_addr = to_addr
        self.smtp_server = smtp_server
        self.thread = None

    @staticmethod
    def format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_email(self, header, text, img_file_name=''):
        msg = MIMEMultipart()
        msg['From'] = EmailHelper.format_addr('你的电脑 <%s>' % self.from_addr)
        msg['To'] = EmailHelper.format_addr('管理员 <%s>' % self.to_addr)
        msg['Subject'] = Header(header, 'utf-8').encode()
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        if img_file_name != '':
            with open(img_file_name, 'rb') as f:
                # 设置附件的MIME和文件名，这里是jpg类型:
                mime = MIMEBase('image', 'jpg', filename=img_file_name)
                # header:
                mime.add_header('Content-Disposition', 'attachment', filename=img_file_name)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # Base64:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)
                # msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
                #             '<p><img src="cid:0"></p>' +
                #             '</body></html>', 'html', 'utf-8'))

        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        server.quit()

    def thread_send_mail(self, header, text, img_file_name=''):
        self.thread = threading.Thread(target=self.send_email, args=(header, text, img_file_name))
        self.thread.start()

    def thread_join(self):
        if self.thread is not None:
            self.thread.join()
