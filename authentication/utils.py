from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Utilities:
    """Utility class that contains helper functions"""

    @staticmethod
    def send_email(data, domain=None, intent=None):
        """This function sends email to users."""
        if intent == 'password_reset':
            url = f"{domain}{data[1]}"
            subject = f"[Expense Tracker] {data[3]}"
            body = "Click the click below to set a new password.\n" + url
            email = EmailMessage(subject, body, to=[data[4]])
            EmailThread(email).start()
        else:
            url = f"http://{get_current_site(data[0]).domain}/api/auth/{data[1]}?token={data[2]}"
            subject = f"[Expense Tracker] {data[3]}"
            body = f"Hello,Click the click below to verify your account.\n{url}"
            email = EmailMessage(subject, body, to=[data[4]])
            EmailThread(email).start()
        return
