from notifications.channels.email_channel_v1 import EmailChannel_v1


class ChannelFactory:
    @staticmethod
    def create_email_channel_v1() -> EmailChannel_v1:
        return EmailChannel_v1(server="smtp.example.com", sender="notifications@example.com")
