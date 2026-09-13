from notifications.notifiers.channel_interface import ChannelInterface


class EmailChannel_v1(ChannelInterface):
    def __init__(self, server, sender):
        self.server = server
        self.sender = sender
        self.is_connected = False

    def connect(self):
        self.is_connected = True
        print(f"Connected to {self.server}")

    def disconnect(self):
        self.is_connected = False
        print(f"Disconnected from {self.server}")

    def deliver(self, message):
        print(f"📧 {self.sender}: {message}")
