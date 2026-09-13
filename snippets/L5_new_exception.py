from notifications.campaigns.campaign_runner_v2 import CampaignRunner_v2
from notifications.notifiers.ai_notifier_v1 import AiNotifier_v1
from notifications.wiring import build_ai_notifier

ai_notifier = build_ai_notifier(AiNotifier_v1)  # the token budget starts empty
runner = CampaignRunner_v2()
runner.start_campaign(ai_notifier)
runner.send_message(ai_notifier, "Your order has shipped! 📦")
# raises: OutOfTokensError: Out of AI tokens! 120 needed but only 0 left
