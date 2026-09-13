from notifications.billing.exceptions import NotEnoughCreditsError


class CampaignRunner_v1:
    def start_campaign(self, notifier):
        notifier.connect()

    def send_message(self, notifier, message):
        try:
            notifier.send(message)
        except NotEnoughCreditsError:
            print("Out of credits, stopping the campaign")
            notifier.disconnect()
