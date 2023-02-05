from twilio.rest import Client
import datetime


def send_sms(to, body):
    # Your Account SID from twilio.com/console
    account_sid = "ACba75a4aabf68f6adfc607b102ab0f322"
    # Your Auth Token from twilio.com/console
    auth_token = "6bf8a4087664523443b1d5a46901535c"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid='MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        to=to,
        from_="+12062087207",
        body=body
    )

    print(message.sid)


def schedule_sms(to, body, time):
    # Your Account SID from twilio.com/console
    account_sid = "ACba75a4aabf68f6adfc607b102ab0f322"
    # Your Auth Token from twilio.com/console
    auth_token = "6bf8a4087664523443b1d5a46901535c"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to,
        from_="+12062087207",
        body='This is a scheduled message',
        schedule_type='fixed',
        send_at=time
    )


if __name__ == "__main__":
    now = datetime.datetime.now()
    two_minutes = now + datetime.timedelta(minutes=2)
    schedule_sms("+919999999999", "Hello from Python!", two_minutes)
