from notifications.audit_log.exceptions import AuditLogDisabledError
from notifications.billing.exceptions import NotEnoughCreditsError
from notifications.notifiers.exceptions import NotConnectedError
from notifications.notifiers.ai_notifier_v2 import AiNotifier_v2


class CampaignRunner_v3:
    """One runner for the whole enterprise demo, so it has to know about every plan."""

    def start_campaign(self, notifier):
        try:
            notifier.connect()
        except AuditLogDisabledError:
            notifier.enable_audit_log()
            notifier.connect()
        if isinstance(notifier, AiNotifier_v2):
            notifier.disable_ai_rewrite()  # save tokens for the big announcement

    def send_message(self, notifier, message):
        try:
            notifier.send(message)
        except (NotEnoughCreditsError, NotConnectedError):
            notifier.disconnect()

    def send_big_announcement(self, notifier, message):
        if isinstance(notifier, AiNotifier_v2):
            notifier.enable_ai_rewrite()
        self.send_message(notifier, message)
        if isinstance(notifier, AiNotifier_v2):
            notifier.disable_ai_rewrite()
