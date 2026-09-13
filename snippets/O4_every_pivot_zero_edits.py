# ...continuing from the previous snippet

# Pivot #2: "push notifications are the future"
push_notifier = Notifier_v4(
    channel=ChannelFactory.create_push_channel_v1(),
    template=TemplateFactory.create_rich_card_template_v1(),
    recipients=RecipientListFactory.create_recipient_list_v1(),
    credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
)

# Pivot #3: "every enterprise lives in Slack"
slack_notifier = Notifier_v4(
    channel=ChannelFactory.create_slack_channel_v1(),
    template=TemplateFactory.create_rich_card_template_v1(),
    recipients=RecipientListFactory.create_recipient_list_v1(),
    credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
)

# Three pivots, one class, zero edits to Notifier_v4
[type(notifier.channel).__name__ for notifier in (sms_notifier, push_notifier, slack_notifier)]
# -> ['SmsChannel_v1', 'PushChannel_v1', 'SlackChannel_v1']
