"""
Yes, Django signals do indeed run in the same database transaction as the caller by default.
 When a signal is triggered by a database operation, it is executed immediately within the same transaction.
  If an exception is raised in either the caller or the signal, the entire transaction, including the caller's changes, will be rolled back.
"""

from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.test import TestCase

# Define a simple model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

# Signal handler that raises an exception
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # Deliberately raise an exception to trigger a rollback
        raise Exception("Simulated exception in signal")

# Test case to verify transactional behavior
class SignalTransactionTest(TestCase):
    def test_signal_transaction(self):
        user_count_before = User.objects.count()
        profile_count_before = Profile.objects.count()

        # Attempt to create a new user
        try:
            with transaction.atomic():
                User.objects.create(username="testuser", password="password")
        except Exception as e:
            print(f"Exception caught: {e}")

        # Check counts after transaction to see if rollback occurred
        user_count_after = User.objects.count()
        profile_count_after = Profile.objects.count()

        print(f"User count before: {user_count_before}, after: {user_count_after}")
        print(f"Profile count before: {profile_count_before}, after: {profile_count_after}")

        # Assert that no new records were created, indicating rollback
        assert user_count_before == user_count_after, "User creation was not rolled back"
        assert profile_count_before == profile_count_after, "Profile creation was not rolled back"
