from django.test import TestCase

# Create your tests here.
from api.models import CustomUser, Profile

class AnimalTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(username="test1", email="test1@gmail.com")
        CustomUser.objects.create(username="test2", email="test2@gmail.com")

    def test_user_creation(self):
        """Animals that can speak are correctly identified"""
        test1 = CustomUser.objects.get(username="test1")
        test2 = CustomUser.objects.get(username="test2")
        self.assertEqual(str(test1), 'test1')
        self.assertEqual(str(test2), 'test2')
    
    def test_profile_creation(self):
        test1 = CustomUser.objects.get(username="test1")
        test2 = CustomUser.objects.get(username="test2")
        Profile.objects.create(user=test1, display_name="Test1", bio="I am a music lover")
        Profile.objects.create(user=test2, display_name="Test2", bio="I am a music lover")
        profile1 = Profile.objects.get(user=test1)
        profile2 = Profile.objects.get(user=test2)
        self.assertEqual(str(profile1), 'Profile of test1')
        self.assertEqual(str(profile2), 'Profile of test2')
        