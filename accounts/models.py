from django.db import models
from django.contrib.auth.models import AbstractUser


class SupervisorProfile(AbstractUser):

    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REVOKED', 'Revoked'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    phone_number = models.CharField(max_length=20, blank=True)

    organization = models.CharField(max_length=100, blank=True)

    assigned_patient_mode = models.CharField(
        max_length=20,
        default='NORMAL',
        choices=[
            ('NORMAL', 'Қалыпты'),
            ('BRADYCARDIA', 'Брадикардия'),
            ('TACHYCARDIA', 'Тахикардия'),
            ('HYPOTENSION', 'Гипотония'),
            ('HYPERTENSION', 'Гипертония'),
            ('MI', 'ЖИИ'),
        ]
    )

    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_users'
    )

    last_connected = models.DateTimeField(null=True, blank=True)

    request_message = models.TextField(
        blank=True,
        help_text="Why do you need access?"
    )

    class Meta:
        verbose_name = 'Supervisor Profile'
        verbose_name_plural = 'Supervisor Profiles'

    def __str__(self):
        return f"{self.username} ({self.get_status_display()})"
