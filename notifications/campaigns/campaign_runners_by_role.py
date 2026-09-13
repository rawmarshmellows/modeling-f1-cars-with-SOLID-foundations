from notifications.billing.exceptions import NotEnoughCreditsError
from notifications.notifiers.exceptions import ConnectRefusedError, NotConnectedError


def connect_or_report(notifier):
    try:
        notifier.connect()
    except ConnectRefusedError as reason:
        print(f"The notifier refused to connect: {reason}")


def send_or_stop(notifier, message):
    try:
        notifier.send(message)
    except (NotEnoughCreditsError, NotConnectedError) as reason:
        print(f"Stopping the campaign: {reason}")
        notifier.disconnect()


class BasicCampaignRunner:
    """For Connectable + Sendable notifiers."""

    def start_campaign(self, notifier):
        connect_or_report(notifier)

    def send_message(self, notifier, message):
        send_or_stop(notifier, message)

    def send_big_announcement(self, notifier, message):
        send_or_stop(notifier, message)


class AuditedCampaignRunner:
    """For Connectable + Sendable + Auditable notifiers: never connects without an audit trail."""

    def start_campaign(self, notifier):
        notifier.enable_audit_log()
        connect_or_report(notifier)

    def send_message(self, notifier, message):
        send_or_stop(notifier, message)

    def send_big_announcement(self, notifier, message):
        send_or_stop(notifier, message)


class AiCampaignRunner:
    """For Connectable + Sendable + Auditable + AiRewritable notifiers: saves tokens for the big announcements."""

    def start_campaign(self, notifier):
        notifier.enable_audit_log()
        connect_or_report(notifier)
        notifier.disable_ai_rewrite()

    def send_message(self, notifier, message):
        send_or_stop(notifier, message)

    def send_big_announcement(self, notifier, message):
        notifier.enable_ai_rewrite()
        send_or_stop(notifier, message)
        notifier.disable_ai_rewrite()
