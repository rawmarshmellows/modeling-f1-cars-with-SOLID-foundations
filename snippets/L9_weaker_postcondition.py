# ...continuing from the previous snippet
def average_credits_per_send(audit_log):
    """Compliance's billing report, written against the promise in NotifierInterface.get_current_audit_entry."""
    credits = [entry["credits_remaining"] for entry in audit_log]
    return (credits[0] - credits[-1]) / (len(credits) - 1)


average_credits_per_send(ai_notifier.get_audit_log())
# raises: KeyError: 'credits_remaining'
