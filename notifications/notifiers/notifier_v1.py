from notifications.billing.credit_balance_v1 import CreditBalance_v1
from notifications.billing.credits import Credits
from notifications.billing.pricing import price_of
from notifications.channels.email_channel_v1 import EmailChannel_v1
from notifications.recipients.recipient_list_v1 import RecipientList_v1
from notifications.templates.html_template_v1 import HtmlTemplate_v1


class Notifier_v1:
    def __init__(self):
        self.channel = self._build_channel()
        self.template = self._build_template()
        self.recipients = self._build_recipients()
        self.credit_balance = self._build_credit_balance()

    def _build_channel(self):
        return EmailChannel_v1(server="smtp.example.com", sender="notifications@example.com")

    def _build_template(self):
        return HtmlTemplate_v1()

    def _build_recipients(self):
        return RecipientList_v1()

    def _build_credit_balance(self):
        return CreditBalance_v1(Credits(1_000))

    def connect(self):
        self.channel.connect()

    def disconnect(self):
        self.channel.disconnect()

    def send(self, message):
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
