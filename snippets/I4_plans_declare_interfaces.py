from notifications.notifiers.segregated_interfaces import (
    AiRewritableInterface,
    AuditableInterface,
    ConnectableInterface,
    SendableInterface,
)


class Notifier_v7(ConnectableInterface, SendableInterface): ...


class AuditedNotifier_v2(ConnectableInterface, SendableInterface, AuditableInterface): ...


class AiNotifier_v3(AuditedNotifier_v2, AiRewritableInterface): ...
