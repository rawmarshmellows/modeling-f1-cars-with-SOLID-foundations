# ...continuing from the previous snippet
ai_notifier = build_ai_notifier(AiNotifier_v1, tokens=4_000)
runner.start_campaign(ai_notifier)  # no AuditLogDisabledError, so the runner never enables the audit log
runner.send_message(ai_notifier, "Your order has shipped! 📦")

ai_notifier.channel.is_connected, ai_notifier.audit_log.is_enabled  # -> (True, False)
ai_notifier.get_audit_log()  # -> []
