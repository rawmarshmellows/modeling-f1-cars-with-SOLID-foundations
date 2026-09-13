from notifications.notifiers.channel_interface import ChannelInterface


class SmsChannel_v1(ChannelInterface):
    def __init__(self):
        self.is_connected = False

    def connect(self):
        self.is_connected = True
        print("Connected to the SMS gateway")

    def disconnect(self):
        self.is_connected = False
        print("Disconnected from the SMS gateway")

    def deliver(self, message):
        print(f"💬 {message}")
