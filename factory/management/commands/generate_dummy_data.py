# yourapp/management/commands/generate_dummy_data.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
import random


class Command(BaseCommand):
    help = 'Generates dummy user data for testing purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of users to generate'
        )

    def handle(self, *args, **options):
        count = options['count']

        self.stdout.write(self.style.SUCCESS(f'Starting to generate {count} dummy users...'))

        try:
            # Generate users in a transaction for atomicity
            with transaction.atomic():
                self._generate_users(count)

            self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} dummy users'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating dummy data: {str(e)}'))

    def _generate_users(self, count):
        """Generate dummy user records"""
        User = get_user_model()

        # Sample data for generation
        roles = ['admin', 'engineer', 'operator']
        role_weights = [0.1, 0.3, 0.6]  # Probability weights

        first_names = ['John', 'Jane', 'Michael', 'Emma', 'Robert', 'Linda', 'William', 'Sarah',
                       'David', 'Jennifer', 'James', 'Lisa', 'Thomas', 'Mary', 'Daniel', 'Patricia']

        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia',
                      'Rodriguez', 'Wilson', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Moore', 'Lee']

        # Generate users
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
            email = f"{username}@example.com"
            role = random.choices(roles, weights=role_weights, k=1)[0]
            phone = f"+1{random.randint(2000000000, 9999999999)}"

            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",  # Default password - should be changed in production
                first_name=first_name,
                last_name=last_name,
                role=role,
                phone=phone
            )

            self.stdout.write(f"Created user: {username} ({role})")