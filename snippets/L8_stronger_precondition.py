# ...continuing from the previous snippet
BIG_SALE_PROMO = "Everything must go! " * 10  # 200 characters, two SMS segments

runner.send_message(ai_notifier, BIG_SALE_PROMO)
# raises: MessageTooLongError: The AI model only rewrites one 160-character segment, got 200 characters
