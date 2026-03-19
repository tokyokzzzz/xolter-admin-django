from django.contrib import admin
from .models import SupervisorProfile


@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'status',
        'assigned_patient_mode', 'last_connected', 'date_joined'
    ]
    list_filter = ['status', 'assigned_patient_mode']
    search_fields = ['username', 'email', 'organization']

    actions = ['approve_users', 'reject_users', 'revoke_users']

    def approve_users(self, request, queryset):
        from django.utils import timezone
        queryset.update(
            status='APPROVED',
            approved_at=timezone.now(),
            approved_by=request.user
        )
        self.message_user(request, f"{queryset.count()} supervisors approved.")
    approve_users.short_description = "✅ Approve selected supervisors"

    def reject_users(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, f"{queryset.count()} supervisors rejected.")
    reject_users.short_description = "❌ Reject selected supervisors"

    def revoke_users(self, request, queryset):
        queryset.update(status='REVOKED')
        self.message_user(request, f"{queryset.count()} supervisors revoked.")
    revoke_users.short_description = "🚫 Revoke access"
