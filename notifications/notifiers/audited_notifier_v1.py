from notifications.audit_log.exceptions import AuditLogDisabledError
from notifications.billing.pricing import price_of
from notifications.notifiers.channel_interface import ChannelInterface
from notifications.notifiers.exceptions import NotConnectedError
from notifications.notifiers.notifier_interface import NotifierInterface


class AuditedNotifier_v1(NotifierInterface):
    def __init__(self, channel: ChannelInterface, template, recipients, credit_balance, audit_log):
        self.channel = channel
        self.template = template
        self.recipients = recipients
        self.credit_balance = credit_balance
        self.audit_log = audit_log

    def connect(self):
        if not self.audit_log.is_enabled:
            raise AuditLogDisabledError("Enable the audit log before connecting!")
        self.channel.connect()

    def disconnect(self):
        self.channel.disconnect()

    def send(self, message):
        self._require_connection()
        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
        self.audit_log.record(self.get_current_audit_entry())

    def _require_connection(self):
        if not self.channel.is_connected:
            raise NotConnectedError("Connect before sending!")

    def enable_audit_log(self):
        self.audit_log.enable()

    def disable_audit_log(self):
        self.disconnect()
        self.audit_log.disable()

    def get_current_audit_entry(self):
        return {"credits_remaining": self.credit_balance.credits.amount}

    def get_audit_log(self):
        return list(self.audit_log.entries)
