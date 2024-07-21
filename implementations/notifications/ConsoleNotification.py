from helpers.MessagingInteface import MessagingInteface
import os


class ConsoleNotification(MessagingInteface):
    def __init__(self, recipients):
        self.recipients = recipients

    def send_message(self, message):
        for recipient in self.recipients:
            print(f"Sending message to {recipient}: {message}")
