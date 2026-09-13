from notifications.campaigns import CampaignRunnerFactory
from notifications.notifiers.ai_notifier_v3 import AiNotifier_v3
from notifications.notifiers.audited_notifier_v2 import AuditedNotifier_v2
from notifications.notifiers.notifier_v7 import Notifier_v7
from notifications.wiring import build_ai_notifier, build_audited_notifier, build_legacy_notifier

demo_plans = [
    build_legacy_notifier(Notifier_v7),
    build_audited_notifier(AuditedNotifier_v2),
    build_ai_notifier(AiNotifier_v3, tokens=4_000),
]
for notifier in demo_plans:
    runner = CampaignRunnerFactory.create_runner_for(notifier)
    runner.start_campaign(notifier)
    runner.send_message(notifier, "Your order has shipped! 📦")
    runner.send_big_announcement(notifier, "🎉 We're live in 40 countries!")

[type(CampaignRunnerFactory.create_runner_for(notifier)).__name__ for notifier in demo_plans]
# -> ['BasicCampaignRunner', 'AuditedCampaignRunner', 'AiCampaignRunner']
