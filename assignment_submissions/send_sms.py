from twilio.rest import Client
import os


def send_sms(to, body):
    # Your Account SID from twilio.com/console
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    # Your Auth Token from twilio.com/console
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to,
        from_=os.environ.get('TWILIO_PHONE_NO'),
        body=body
    )

    print(message.sid)
