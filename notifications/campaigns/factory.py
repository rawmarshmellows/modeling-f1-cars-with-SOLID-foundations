from notifications.campaigns.campaign_runners_by_role import AiCampaignRunner, AuditedCampaignRunner, BasicCampaignRunner
from notifications.notifiers.segregated_interfaces import (
    AiRewritableInterface,
    AuditableInterface,
    ConnectableInterface,
    SendableInterface,
)


class CampaignRunnerFactory:
    @staticmethod
    def create_runner_for(notifier):
        name = type(notifier).__name__
        if not (isinstance(notifier, ConnectableInterface) and isinstance(notifier, SendableInterface)):
            raise TypeError(f"{name} can't run a campaign: it isn't Connectable and Sendable")
        if isinstance(notifier, AuditableInterface) and isinstance(notifier, AiRewritableInterface):
            return AiCampaignRunner()
        if isinstance(notifier, AuditableInterface):
            return AuditedCampaignRunner()
        if isinstance(notifier, AiRewritableInterface):
            raise TypeError(f"No campaign runner handles AI rewrites without an audit log yet ({name})")
        return BasicCampaignRunner()
