from django.db import models  # Must be first import
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrator'),
        ('engineer', 'Engineer'),
        ('operator', 'Operator'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='operator')
    phone = models.CharField(max_length=20, blank=True)

    # Add these to resolve conflicts
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="factory_user_groups",
        related_query_name="factory_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="factory_user_permissions",
        related_query_name="factory_user",
    )

    class Meta:
        # Add this if not already present
        swappable = 'AUTH_USER_MODEL'