from abc import ABC, abstractmethod


class ConnectableInterface(ABC):
    @abstractmethod
    def connect(self):
        """Raises ConnectRefusedError (or a subclass of it) if the notifier isn't ready to connect."""

    @abstractmethod
    def disconnect(self): ...


class SendableInterface(ABC):
    @abstractmethod
    def send(self, message):
        """Sends a message of any length, charging exactly one credit per 160-character segment.

        Raises NotConnectedError before connect(), NotEnoughCreditsError when the credits
        run out, and nothing else.
        """


class AuditableInterface(ABC):
    """Invariant: nothing is ever sent while the audit log is off.

    connect() refuses with AuditLogDisabledError (a ConnectRefusedError) without an audit log,
    and disable_audit_log() disconnects first.
    """

    @abstractmethod
    def enable_audit_log(self): ...

    @abstractmethod
    def disable_audit_log(self):
        """Disconnects first, so nothing is ever sent unaudited."""

    @abstractmethod
    def get_current_audit_entry(self):
        """A snapshot of the notifier that always includes "credits_remaining"."""

    @abstractmethod
    def get_audit_log(self):
        """Every entry recorded since the audit log was enabled, oldest first.

        The log is append-only: an entry, once recorded, never disappears.
        """


class AiRewritableInterface(ABC):
    @abstractmethod
    def enable_ai_rewrite(self): ...

    @abstractmethod
    def disable_ai_rewrite(self): ...
