import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Gmail:

    def __init__(self, login_mail_box, password_mail_box) -> None:

        self.GMAIL_SMTP = "smtp.gmail.com"
        self.GMAIL_IMAP = "imap.gmail.com"
        self.login = login_mail_box
        self.password = password_mail_box
    #send message

    def send_message(self, recipients, subject, text_message):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(text_message))
        mail = smtplib.SMTP(self.GMAIL_SMTP, 587)
        mail.ehlo()
        mail.starttls()
        mail.ehlo()
        mail.login(self.login, self.password)
        mail.sendmail(self.login, recipients, msg.as_string())
        mail.quit()

    def get_message(self, header):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email).decode('utf-8')
        mail.logout()

login = 'login@gmail.com'
password = 'qwerty'
subject = 'Subject'
recipients = ['vasya@email.com', 'petya@email.com']
message = 'Message'
header = None


if __name__ == "__main__":
    my_gmail = Gmail(login_mail_box=login, password_mail_box=password)
    my_gmail.send_message(subject=subject, recipients=recipients, text_message=message)
    my_gmail.get_message(header)
