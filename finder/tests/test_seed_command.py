from io import StringIO

from django.contrib.auth import authenticate
from django.core.management import call_command
from django.test import TestCase

from finder.models import Interest, ProjectIdea, StaffProfile, User


class SeedCommandTests(TestCase):
    def test_seed_command_creates_fictional_dataset_and_logins(self):
        output = StringIO()
        call_command("seed_demo", stdout=output)

        self.assertEqual(User.objects.count(), 6)
        self.assertEqual(StaffProfile.objects.count(), 5)
        self.assertEqual(Interest.objects.count(), 15)
        self.assertEqual(ProjectIdea.objects.count(), 10)
        self.assertIn("fictional demo data", output.getvalue())

        student = authenticate(
            email="student@example.test",
            password="Student1234.",
        )
        staff = authenticate(
            email="staff@example.test",
            password="Staff1234.",
        )
        self.assertIsNotNone(student)
        self.assertIsNotNone(staff)
        self.assertTrue(student.groups.filter(name="Student").exists())
        self.assertTrue(staff.groups.filter(name="Staff").exists())
        self.assertNotEqual(student.password, "Student1234.")
        self.assertNotEqual(staff.password, "Staff1234.")

    def test_seed_command_is_repeatable(self):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_demo", stdout=StringIO())
        self.assertEqual(User.objects.count(), 6)
        self.assertEqual(StaffProfile.objects.count(), 5)
        self.assertEqual(Interest.objects.count(), 15)
        self.assertEqual(ProjectIdea.objects.count(), 10)

        extra_staff = User.objects.get(email="liam.chen@example.test")
        self.assertFalse(extra_staff.has_usable_password())
