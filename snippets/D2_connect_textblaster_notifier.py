from notifications.billing import CreditBalanceFactory
from notifications.campaigns.campaign_runner_v1 import CampaignRunner_v1
from notifications.channels import ChannelFactory
from notifications.notifiers.notifier_v4 import Notifier_v4
from notifications.recipients import RecipientListFactory
from notifications.templates import TemplateFactory

textblaster_notifier = Notifier_v4(
    channel=ChannelFactory.create_textblaster_sms_channel_v1(),
    template=TemplateFactory.create_plain_text_template_v1(),
    recipients=RecipientListFactory.create_recipient_list_v1(),
    credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
)
runner = CampaignRunner_v1()
runner.start_campaign(textblaster_notifier)
# raises: AttributeError: 'TextBlasterSmsChannel_v1' object has no attribute 'connect'
