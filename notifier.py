from twilio.rest import Client

class SendText(object):
    def __init__(self, send_to, sent_from, text_body, account_sid = "", account_auth=""):
        super(SendText, self).__init__()
        self.send_to = send_to
        self.sent_from = sent_from
        self.text_body = text_body
        self.account_sid = account_sid
        self.account_auth = account_auth

    def _send(self):
        client = Client(self.account_sid, self.account_auth)
        client.messages.create(
            to=self.send_to,
            from_=self.sent_from,
            body=self.text_body
        )
