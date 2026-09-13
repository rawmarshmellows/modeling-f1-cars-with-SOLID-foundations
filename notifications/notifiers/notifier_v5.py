from notifications.billing.pricing import price_of
from notifications.notifiers.channel_interface import ChannelInterface


class Notifier_v5:
    def __init__(self, channel: ChannelInterface, template, recipients, credit_balance):
        self.channel = channel
        self.template = template
        self.recipients = recipients
        self.credit_balance = credit_balance

    def connect(self):
        self.channel.connect()

    def disconnect(self):
        self.channel.disconnect()

    def send(self, message):
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
