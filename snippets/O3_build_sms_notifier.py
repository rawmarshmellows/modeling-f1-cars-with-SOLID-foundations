from notifications.billing import CreditBalanceFactory
from notifications.channels import ChannelFactory
from notifications.notifiers.notifier_v4 import Notifier_v4
from notifications.recipients import RecipientListFactory
from notifications.templates import TemplateFactory

sms_notifier = Notifier_v4(
    channel=ChannelFactory.create_sms_channel_v1(),
    template=TemplateFactory.create_plain_text_template_v1(),
    recipients=RecipientListFactory.create_recipient_list_v1(),
    credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
)
sms_notifier.connect()
sms_notifier.send("Your order has shipped! 📦")
sms_notifier.credit_balance.credits.amount  # -> 999
