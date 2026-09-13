from notifications.billing.pricing import price_of
from notifications.channels.sms_channel_v1 import SmsChannel_v1
from notifications.channels.textblaster_sms_channel_v1 import TextBlasterSmsChannel_v1


class Notifier_v4_patched:
    def __init__(self, channel, template, recipients, credit_balance):
        self.channel = channel
        self.template = template
        self.recipients = recipients
        self.credit_balance = credit_balance

    def connect(self):
        channel_type = type(self.channel)
        if channel_type == SmsChannel_v1:
            self.channel.connect()
        elif channel_type == TextBlasterSmsChannel_v1:
            self.channel.open_socket()

    def disconnect(self):
        self.channel.disconnect()

    def send(self, message):
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
