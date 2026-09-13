# ...continuing: build_ai_notifier, CampaignRunner_v2, BIG_SALE_PROMO and average_credits_per_send come from above
from notifications.notifiers.ai_notifier_v2 import AiNotifier_v2
from notifications.notifiers.audited_notifier_v1 import AuditedNotifier_v1
from notifications.wiring import build_audited_notifier

notifiers = [
    build_audited_notifier(AuditedNotifier_v1),
    build_ai_notifier(AiNotifier_v2, tokens=4_000),  # AI rewrites on this time
]
runner = CampaignRunner_v2()  # not a single line of the runner has changed
for notifier in notifiers:
    runner.start_campaign(notifier)
    for _ in range(10):
        runner.send_message(notifier, BIG_SALE_PROMO)

[len(notifier.get_audit_log()) for notifier in notifiers]  # -> [10, 10]
[average_credits_per_send(notifier.get_audit_log()) for notifier in notifiers]  # -> [2.0, 2.0]
