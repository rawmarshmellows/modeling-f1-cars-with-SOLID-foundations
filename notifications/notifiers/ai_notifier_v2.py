from notifications.ai.tokens import Tokens
from notifications.billing.pricing import price_of, segments_of
from notifications.notifiers.ai_channel_interface import AiChannelInterface
from notifications.notifiers.audited_notifier_v1 import AuditedNotifier_v1


class AiNotifier_v2(AuditedNotifier_v1):
    """AI-powered notifications, built to stand in for any NotifierInterface notifier.

    connect and get_audit_log are inherited untouched, so the audit invariant
    and the audit history both survive.
    """

    TOKENS_PER_SEGMENT = Tokens(120)

    def __init__(self, channel: AiChannelInterface, template, recipients, credit_balance, audit_log, token_budget):
        super().__init__(channel, template, recipients, credit_balance, audit_log)
        self.token_budget = token_budget
        self.ai_rewrite_is_enabled = True

    def send(self, message):
        self._require_connection()
        segments = segments_of(message)
        # One credit per segment. The model rewrites a segment into a segment, so rewriting can't change the bill.
        self.credit_balance.charge(price_of(message))

        # No new exceptions: not enough tokens means no rewrite, not a crash
        rewrite_cost = Tokens(self.TOKENS_PER_SEGMENT.amount * len(segments))
        if self.ai_rewrite_is_enabled and self.token_budget.can_afford(rewrite_cost):
            self.token_budget.spend(rewrite_cost)
            # No stronger precondition: long messages are rewritten one segment at a time
            segments = [self.channel.rewrite_with_ai(segment) for segment in segments]

        for segment in segments:
            self.channel.deliver(segment)
        self.audit_log.record(self.get_current_audit_entry())

    def enable_ai_rewrite(self):
        self.ai_rewrite_is_enabled = True

    def disable_ai_rewrite(self):
        self.ai_rewrite_is_enabled = False

    def get_current_audit_entry(self):
        # No weaker postcondition: everything the parent reported, plus the token budget
        return {
            **super().get_current_audit_entry(),
            "tokens_remaining": self.token_budget.tokens.amount,
        }
