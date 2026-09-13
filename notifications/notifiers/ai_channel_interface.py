from abc import abstractmethod

from notifications.notifiers.channel_interface import ChannelInterface


class AiChannelInterface(ChannelInterface):
    @abstractmethod
    def rewrite_with_ai(self, segment):
        """Rewrites one SMS segment and returns one SMS segment.

        Raises MessageTooLongError for anything longer than 160 characters.
        """
