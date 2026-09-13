from notifications.billing.pricing import SEGMENT_LENGTH
from notifications.channels.exceptions import MessageTooLongError
from notifications.notifiers.ai_channel_interface import AiChannelInterface


class AiSmsChannel_v1(AiChannelInterface):
    def __init__(self):
        self.is_connected = False

    def connect(self):
        self.is_connected = True
        print("Connected to the AI SMS gateway")

    def disconnect(self):
        self.is_connected = False
        print("Disconnected from the AI SMS gateway")

    def deliver(self, message):
        print(f"💬 {message}")

    def rewrite_with_ai(self, segment):
        if len(segment) > SEGMENT_LENGTH:
            raise MessageTooLongError(
                f"The AI model only rewrites one {SEGMENT_LENGTH}-character segment, got {len(segment)} characters"
            )
        print("✨ Made it pop")
        return segment  # the model's edits are left as an exercise for the board
