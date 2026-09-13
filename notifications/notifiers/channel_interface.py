from abc import ABC, abstractmethod


class ChannelInterface(ABC):
    """The notifier team's spec: what every channel must do to plug into one of our notifiers."""

    is_connected: bool

    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def deliver(self, message): ...
