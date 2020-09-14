import smtplib
from config import user_config
from email.mime.text import MIMEText


class EmailHelper(object):

    def __init__(self, receiver_email: str):
        self._smtp_host = user_config.get("SMTP_HOST")
        self._smtp_user = user_config.get("SMTP_USER")
        self._smtp_pass = user_config.get("SMTP_PASS")
        self._receiver = receiver_email

    def _check_smtp_config(self):
        if (
            self._smtp_host is None or
            self._smtp_user is None or
            self._smtp_pass is None or
            self._receiver is None
        ):
            raise Exception("SMTP configuration is not completed")

    def send_email(self, subject: str = None, content: str = None):
        self._check_smtp_config()
        if subject is None:
            subject = f"Message from {self._smtp_user}"
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = self._smtp_user
        message['To'] = self._receiver
        message["Subject"] = subject

        # try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(self._smtp_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(self._smtp_user, self._smtp_pass)
        smtpObj.sendmail(self._smtp_user, self._receiver, message.as_string())
        # except:
        #     print(f"[EMAIL_HELPER]: Failed while sending email to {self._receiver}")

    def send_token(self, token):
        self.send_email(
            subject="测试验证码",
            content=f"验证码：{token}"
        )

