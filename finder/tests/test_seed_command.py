from io import StringIO

from django.contrib.auth import authenticate
from django.core.management import call_command
from django.test import TestCase

from finder.demo_accounts import STAFF_ACCOUNTS, STUDENT_ACCOUNTS
from finder.models import Interest, ProjectIdea, StaffProfile, User


class SeedCommandTests(TestCase):
    def test_seed_command_creates_fictional_dataset_and_logins(self):
        output = StringIO()
        call_command("seed_demo", stdout=output)

        self.assertEqual(User.objects.count(), 8)
        self.assertEqual(StaffProfile.objects.count(), 5)
        self.assertEqual(Interest.objects.count(), 15)
        self.assertEqual(ProjectIdea.objects.count(), 10)
        self.assertIn("fictional demo data", output.getvalue())

        for account in STUDENT_ACCOUNTS:
            with self.subTest(role="Student", email=account["email"]):
                student = authenticate(
                    email=account["email"],
                    password=account["password"],
                )
                self.assertIsNotNone(student)
                self.assertTrue(student.groups.filter(name="Student").exists())
                self.assertNotEqual(student.password, account["password"])

        for account in STAFF_ACCOUNTS:
            with self.subTest(role="Staff", email=account["email"]):
                staff = authenticate(
                    email=account["email"],
                    password=account["password"],
                )
                self.assertIsNotNone(staff)
                self.assertTrue(staff.groups.filter(name="Staff").exists())
                self.assertTrue(hasattr(staff, "staff_profile"))
                self.assertNotEqual(staff.password, account["password"])

    def test_seed_command_is_repeatable(self):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_demo", stdout=StringIO())
        self.assertEqual(User.objects.count(), 8)
        self.assertEqual(StaffProfile.objects.count(), 5)
        self.assertEqual(Interest.objects.count(), 15)
        self.assertEqual(ProjectIdea.objects.count(), 10)

        for account in (*STUDENT_ACCOUNTS, *STAFF_ACCOUNTS):
            with self.subTest(email=account["email"]):
                user = User.objects.get(email=account["email"])
                self.assertTrue(user.has_usable_password())
                self.assertTrue(user.check_password(account["password"]))
