# ...continuing from the previous snippet
ai_notifier.enable_audit_log()  # enable it by hand this time
runner.send_message(ai_notifier, "Your order has shipped! 📦")
first_entry = ai_notifier.get_audit_log()[0]

for _ in range(9):
    runner.send_message(ai_notifier, "Your order has shipped! 📦")

first_entry in ai_notifier.get_audit_log()  # -> False
len(ai_notifier.get_audit_log())  # -> 5
