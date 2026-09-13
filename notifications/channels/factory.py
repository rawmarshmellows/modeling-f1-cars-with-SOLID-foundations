from notifications.channels.ai_sms_channel_v1 import AiSmsChannel_v1
from notifications.channels.email_channel_v1 import EmailChannel_v1
from notifications.channels.push_channel_v1 import PushChannel_v1
from notifications.channels.slack_channel_v1 import SlackChannel_v1
from notifications.channels.sms_channel_v1 import SmsChannel_v1
from notifications.channels.textblaster_sms_channel_v1 import TextBlasterSmsChannel_v1
from notifications.channels.textblaster_sms_channel_v2 import TextBlasterSmsChannel_v2
from notifications.channels.textblaster_sms_channel_v3 import TextBlasterSmsChannel_v3


class ChannelFactory:
    @staticmethod
    def create_email_channel_v1() -> EmailChannel_v1:
        return EmailChannel_v1(server="smtp.example.com", sender="notifications@example.com")

    @staticmethod
    def create_sms_channel_v1() -> SmsChannel_v1:
        return SmsChannel_v1()

    @staticmethod
    def create_push_channel_v1() -> PushChannel_v1:
        return PushChannel_v1()

    @staticmethod
    def create_slack_channel_v1() -> SlackChannel_v1:
        return SlackChannel_v1()

    @staticmethod
    def create_textblaster_sms_channel_v1() -> TextBlasterSmsChannel_v1:
        return TextBlasterSmsChannel_v1()

    @staticmethod
    def create_textblaster_sms_channel_v2() -> TextBlasterSmsChannel_v2:
        return TextBlasterSmsChannel_v2()

    @staticmethod
    def create_textblaster_sms_channel_v3() -> TextBlasterSmsChannel_v3:
        return TextBlasterSmsChannel_v3()

    @staticmethod
    def create_ai_sms_channel_v1() -> AiSmsChannel_v1:
        return AiSmsChannel_v1()
