class TextBlasterSmsChannel_v1:
    """TextBlaster's SMS SDK: cheaper, and it opens a socket instead of connecting."""

    def __init__(self):
        self.is_connected = False

    def open_socket(self):
        self.is_connected = True
        print("TextBlaster socket opened")

    def disconnect(self):
        self.is_connected = False
        print("TextBlaster socket closed")

    def deliver(self, message):
        print(f"💬 (via TextBlaster) {message}")
