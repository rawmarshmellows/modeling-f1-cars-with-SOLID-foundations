from notifications.notifiers.exceptions import ConnectRefusedError


class AuditLogDisabledError(ConnectRefusedError):
    pass
