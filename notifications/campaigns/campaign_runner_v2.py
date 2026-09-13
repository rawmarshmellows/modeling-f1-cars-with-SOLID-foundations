from notifications.audit_log.exceptions import AuditLogDisabledError
from notifications.billing.exceptions import NotEnoughCreditsError
from notifications.notifiers.exceptions import NotConnectedError


class CampaignRunner_v2:
    """Written against NotifierInterface: its signatures and its docstrings."""

    def start_campaign(self, notifier):
        try:
            notifier.connect()
        except AuditLogDisabledError:
            print("The audit log is off, enabling it and trying again...")
            notifier.enable_audit_log()
            notifier.connect()

    def send_message(self, notifier, message):
        try:
            notifier.send(message)
        except (NotEnoughCreditsError, NotConnectedError) as reason:
            print(f"Stopping the campaign: {reason}")
            notifier.disconnect()
