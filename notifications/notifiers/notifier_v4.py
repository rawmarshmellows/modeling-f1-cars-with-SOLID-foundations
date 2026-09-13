from notifications.billing.pricing import price_of


class Notifier_v4:
    def __init__(self, channel, template, recipients, credit_balance):
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
