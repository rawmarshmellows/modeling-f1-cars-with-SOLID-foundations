from notifications.billing.pricing import price_of
from notifications.notifiers.channel_interface import ChannelInterface
from notifications.notifiers.exceptions import NotConnectedError
from notifications.notifiers.notifier_interface import NotifierInterface


class Notifier_v6(NotifierInterface):
    """The legacy email plan, squeezed into NotifierInterface for the enterprise demo."""

    def __init__(self, channel: ChannelInterface, template, recipients, credit_balance):
        self.channel = channel
        self.template = template
        self.recipients = recipients
        self.credit_balance = credit_balance

    def connect(self):
        # Can't keep the invariant: there's no audit log to check
        self.channel.connect()

    def disconnect(self):
        self.channel.disconnect()

    def send(self, message):
        if not self.channel.is_connected:
            raise NotConnectedError("Connect before sending!")
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)

    # The legacy plan never had an audit log, but NotifierInterface insists on one
    def enable_audit_log(self):
        pass  # nothing to switch on

    def disable_audit_log(self):
        pass  # nothing to switch off

    def get_current_audit_entry(self):
        return {}  # nowhere to record it, so the "always includes credits_remaining" promise is broken

    def get_audit_log(self):
        return []  # looks exactly like "someone forgot to enable the audit log"
