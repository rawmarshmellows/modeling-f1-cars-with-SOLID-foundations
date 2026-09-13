from notifications.notifiers.channel_interface import ChannelInterface


class SlackChannel_v1(ChannelInterface):
    def __init__(self):
        self.is_connected = False

    def connect(self):
        self.is_connected = True
        print("Connected to the Slack workspace")

    def disconnect(self):
        self.is_connected = False
        print("Disconnected from the Slack workspace")

    def deliver(self, message):
        print(f"#️⃣ {message}")
