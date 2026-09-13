from notifications.ai.tokens import Tokens
from notifications.billing.pricing import price_of
from notifications.notifiers.ai_channel_interface import AiChannelInterface
from notifications.notifiers.audited_notifier_v1 import AuditedNotifier_v1


class AiNotifier_v1(AuditedNotifier_v1):
    """AI-powered notifications, shipped by Friday. Each change looks reasonable, and each one breaks the contract."""

    TOKENS_PER_REWRITE = Tokens(120)
    MAX_AUDIT_ENTRIES = 5

    def __init__(self, channel: AiChannelInterface, template, recipients, credit_balance, audit_log, token_budget):
        super().__init__(channel, template, recipients, credit_balance, audit_log)
        self.token_budget = token_budget
        self.ai_rewrite_is_enabled = True

    def connect(self):
        # "The AI logs everything anyway, the audit check is redundant"
        self.channel.connect()

    def send(self, message):
        self._require_connection()
        # "AI on by default, that's the whole point"
        if self.ai_rewrite_is_enabled:
            self.token_budget.spend(self.TOKENS_PER_REWRITE)  # OutOfTokensError on an empty budget
            # "Nobody reads past 160 characters anyway"
            message = self.channel.rewrite_with_ai(message)  # MessageTooLongError past one segment

        self.credit_balance.charge(price_of(message))
        self.channel.deliver(message)
        self.audit_log.record(self.get_current_audit_entry())
        # "Storage isn't free, only keep the recent entries"
        del self.audit_log.entries[: -self.MAX_AUDIT_ENTRIES]

    def enable_ai_rewrite(self):
        self.ai_rewrite_is_enabled = True

    def disable_ai_rewrite(self):
        self.ai_rewrite_is_enabled = False

    def get_current_audit_entry(self):
        # "The board only asks about AI"
        return {"tokens_remaining": self.token_budget.tokens.amount}
