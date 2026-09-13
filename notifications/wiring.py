"""The composition root: the one place that decides which parts go into which notifier.

Later examples use these builders so the snippets can focus on behaviour, not wiring.
When Pat changes the requirements, this is usually the only file that has to change.
"""

from notifications.ai import TokenBudgetFactory
from notifications.audit_log import AuditLogFactory
from notifications.billing import CreditBalanceFactory
from notifications.channels import ChannelFactory
from notifications.notifiers.notifier_v5 import Notifier_v5
from notifications.recipients import RecipientListFactory
from notifications.templates import TemplateFactory


def build_production_notifier():
    """Whatever Pat asked for most recently."""
    return Notifier_v5(
        channel=ChannelFactory.create_slack_channel_v1(),
        template=TemplateFactory.create_rich_card_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )


def build_legacy_notifier(notifier_class):
    return notifier_class(
        channel=ChannelFactory.create_email_channel_v1(),
        template=TemplateFactory.create_html_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
    )


def build_audited_notifier(notifier_class):
    return notifier_class(
        channel=ChannelFactory.create_textblaster_sms_channel_v3(),
        template=TemplateFactory.create_plain_text_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
        audit_log=AuditLogFactory.create_audit_log_v1(),
    )


def build_ai_notifier(notifier_class, tokens=0):
    return notifier_class(
        channel=ChannelFactory.create_ai_sms_channel_v1(),
        template=TemplateFactory.create_plain_text_template_v1(),
        recipients=RecipientListFactory.create_recipient_list_v1(),
        credit_balance=CreditBalanceFactory.create_credit_balance_v1(),
        audit_log=AuditLogFactory.create_audit_log_v1(),
        token_budget=TokenBudgetFactory.create_token_budget_v1(tokens),
    )
