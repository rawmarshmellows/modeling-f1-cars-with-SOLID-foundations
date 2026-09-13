class ConnectRefusedError(Exception):
    """The notifier isn't ready to connect, and says why."""


class NotConnectedError(Exception):
    """Something tried to send before connect() succeeded."""
