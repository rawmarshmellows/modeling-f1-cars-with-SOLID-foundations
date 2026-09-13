# ...continuing from the previous snippet
from notifications.notifiers.notifier_v5 import Notifier_v5

textblaster_notifier = Notifier_v5(
    channel=ChannelFactory.create_textblaster_sms_channel_v3(),
    template=TemplateFactory.create_plain_text_template_v1(),
    recipients=RecipientListFactory.create_recipient_list_v1(),
    credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
)
runner.start_campaign(textblaster_notifier)  # the same CampaignRunner_v1, and a notifier that's never heard of TextBlaster
textblaster_notifier.channel.is_connected  # -> True
