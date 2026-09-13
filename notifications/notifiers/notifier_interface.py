from abc import ABC, abstractmethod


class NotifierInterface(ABC):
    """Every notifier we've shipped since compliance got involved.

    The signatures are half of the contract. The docstrings are the other half,
    and the campaign runners and the compliance team rely on both.

    Invariant: nothing is ever sent while the audit log is off. connect() refuses
    without an audit log, send() refuses without a connection, and disable_audit_log()
    disconnects first.
    """

    @abstractmethod
    def connect(self):
        """Raises AuditLogDisabledError instead of connecting without an audit trail."""

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def send(self, message):
        """Sends a message of any length, charging exactly one credit per 160-character segment.

        Raises NotConnectedError before connect(), NotEnoughCreditsError when the credits
        run out, and nothing else.
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
