from notifications.billing.pricing import price_of
from notifications.notifiers.channel_interface import ChannelInterface
from notifications.notifiers.exceptions import NotConnectedError
from notifications.notifiers.segregated_interfaces import ConnectableInterface, SendableInterface


class Notifier_v7(ConnectableInterface, SendableInterface):
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
        if not self.channel.is_connected:
            raise NotConnectedError("Connect before sending!")
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
