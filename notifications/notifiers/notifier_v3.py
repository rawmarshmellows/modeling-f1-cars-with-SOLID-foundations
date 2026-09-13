from notifications.billing import CreditBalanceFactory
from notifications.billing.pricing import price_of
from notifications.channels import ChannelFactory
from notifications.recipients import RecipientListFactory
from notifications.templates import TemplateFactory


class Notifier_v3:
    def __init__(self):
        self.channel = ChannelFactory.create_sms_channel_v1()
        self.template = TemplateFactory.create_html_template_v1()
        self.recipients = RecipientListFactory.create_recipient_list_v1()
        self.credit_balance = CreditBalanceFactory.create_credit_balance_v1()

    def connect(self):
        self.channel.connect()

    def disconnect(self):
        self.channel.disconnect()

    def send(self, message):
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
