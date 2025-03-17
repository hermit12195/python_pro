from datetime import timedelta
from unittest.mock import patch
from django.core.mail import send_mail
from django.test import TestCase
from django.utils import timezone
from .models import User, Category, Ad, Comment
from .signals import remove_handler


class UserTestCase(TestCase):
    """
    Test case for the User model and its associated methods.

    This test case validates the functionality of the User model, particularly:
    - The correct retrieval of user address and phone number.
    - The ability to fetch the list of ads associated with a user.

    Methods:
        test_user_address: Verifies the user's address.
        test_user_phone_number: Verifies the user's phone number.
        test_ads_list: Verifies the list of ads associated with the user.
    """
    def setUp(self):
        user = User.objects.create(username="TestVlad", password="TestPass", phone_number='123456789123',
                                   address="TestAdr")
        Ad.objects.create(title="test", description="test", price=1, created_at=timezone.now(),
                          updated_at=timezone.now(), is_active=True, user=user)

    def test_user_address(self):
        """
        Verifies that the user's address is correctly stored in the database.
        """
        user = User.objects.get(username="TestVlad")
        self.assertEqual(user.address, "TestAdr")

    def test_user_phone_number(self):
        """
        Verifies that the user's phone number is correctly stored in the database.
        """
        user = User.objects.get(username="TestVlad")
        self.assertEqual(user.phone_number, '123456789123')

    def test_ads_list(self):
        """
        Verifies that the user's ads list method works correctly, returning the
        list of ads associated with the user.
        """
        user = User.objects.get(username="TestVlad")
        self.assertEqual(len(user.ads_list()), 1)


class CategoryTestCase(TestCase):
    """
    Test case for the Category model and its associated methods.

    This test case validates the functionality of the Category model, particularly:
    - Verifying the number of active ads associated with a category.

    Methods:
        test_active_ads: Verifies the number of active ads in a category.
    """
    def setUp(self):
        user = User.objects.create(username="TestVlad", password="TestPass", phone_number='123456789123',
                                   address="TestAdr")
        category = Category.objects.create(name="Test", description="Test")
        ad = Ad.objects.create(title="test", description="test", price=1, created_at=timezone.now(),
                               updated_at=timezone.now(), is_active=True, user=user)
        ad.category.set([category])

    def test_active_ads(self):
        """
        Verifies that the correct number of active ads are returned for a given category.
        """
        category = Category.objects.get(name="Test")
        self.assertEqual(category.active_ads(), 1)


class AdTestCase(TestCase):
    """
    Test case for the Ad model and its associated methods.

    This test case validates the functionality of the Ad model, particularly:
    - Verifying the functionality of the short description method.
    - Verifying the correct count of comments associated with an ad.

    Methods:
        test_short_description: Verifies that the short description of the ad is correctly formatted.
        test_comment_number: Verifies that the number of comments for the ad is correctly counted.
    """
    def setUp(self):
        user = User.objects.create(username="TestVlad", password="TestPass", phone_number='123456789123',
                                   address="TestAdr")
        ad = Ad.objects.create(title="test", description="test", price=1, created_at=timezone.now(),
                               updated_at=timezone.now(), is_active=True, user=user)
        comment = Comment.objects.create(content="Test", created_at=timezone.now())
        comment.ad.set([ad])
        comment.user.set([user])

    def test_short_description(self):
        """
        Verifies that the short description method of the ad correctly returns
        the truncated description (with ellipsis).
        """
        ad = Ad.objects.get(title="test")
        self.assertEqual(ad.short_description(), "test...")

    def test_comment_number(self):
        """
        Verifies that the comments_number method of the ad correctly returns
        the number of comments associated with the ad.
        """
        ad = Ad.objects.get(title="test")
        self.assertEqual(ad.comments_number(), 1)


class RemoveHandlerSignalTestCase(TestCase):
    """
    Test case for testing the removal of old ads through a signal handler.

    This test case ensures that ads older than 30 days are correctly marked as inactive
    when the remove_handler function is executed. It simulates a scenario where an ad
    is older than 30 days and verifies that its 'is_active' field is set to False.

    Methods:
        test_remove_old_ads: Verifies that old ads are correctly marked as inactive.
    """
    def setUp(self):
        user = User.objects.create(username="TestVlad", password="TestPass", phone_number='123456789123',
                                   address="TestAdr")
        ad = Ad.objects.create(title="test", description="test", price=1,
                               updated_at=timezone.now(), is_active=True, user=user)
        Ad.objects.filter(id=ad.id).update(created_at=timezone.now() - timedelta(days=40))

    def test_remove_old_ads(self):
        """
        Verifies that old ads (older than 30 days) are correctly marked as inactive
        by the remove_handler signal function.
        """
        remove_handler(Ad)
        ad = Ad.objects.get(title="test")
        self.assertFalse(ad.is_active)
