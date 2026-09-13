from notifications.audit_log.audit_log_v1 import AuditLog_v1


class AuditLogFactory:
    @staticmethod
    def create_audit_log_v1():
        return AuditLog_v1()
