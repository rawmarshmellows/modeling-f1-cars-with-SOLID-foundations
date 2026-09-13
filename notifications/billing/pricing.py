from notifications.billing.credits import Credits

SEGMENT_LENGTH = 160


def segments_of(message):
    """SMS is billed per 160-character segment, and even a one-word message is one segment."""
    return [message[start:start + SEGMENT_LENGTH] for start in range(0, len(message), SEGMENT_LENGTH)] or [message]


def price_of(message):
    return Credits(len(segments_of(message)))
