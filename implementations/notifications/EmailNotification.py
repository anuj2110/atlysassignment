from helpers.MessagingInteface import MessagingInteface
import os
import aiohttp


class EmailNotification(MessagingInteface):
    def __init__(self, recipient_emails):
        self.recipient_emails = recipient_emails

    def make_brevo_data(self, data):
        body_data = {
            "sender": {
                "name": "",
                "email": ""
            },
            "to": [
                {
                    "email": data.get('recipient_email')
                }
            ],
            "subject": "Reminder from FastScraper",
            "htmlContent":""
        }
        body_data['htmlContent'] = f"<p>{data.get('content')}</p>"
        body_data["sender"] = {
            "email": data.get("sender_email")
        }
        return body_data

    async def send_message(self, message):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-key': os.getenv('BREVO_API_KEY')
        }
        for email in self.recipient_emails:
            async with aiohttp.ClientSession() as session:
                async with session.post(os.environ.get("BREVO_URL"), headers=headers, json=self.make_brevo_data({
                    "recipient_email": email,
                    "sender_email": 'atrehan1098@gmail.com',
                    "sender_name": 'FastScraper',
                    "content": message

                })) as response:
                    if response.status==201:
                        print("email sent")
                    else:
                        print("email not sent")
            print(f"Sending email: '{message}' to {email}")
