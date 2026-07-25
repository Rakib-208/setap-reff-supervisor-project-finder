from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from finder.models import Interest, ProjectIdea, StaffProfile, User

from .base import FinderTestCase


class UserModelTests(FinderTestCase):
    def test_user_manager_requires_email(self):
        with self.assertRaisesMessage(ValueError, "email address is required"):
            User.objects.create_user(email="", password="StrongPassword123.")

    def test_user_manager_normalises_email_domain(self):
        user = User.objects.create_user(
            email="CaseSensitive@EXAMPLE.TEST",
            password="StrongPassword123.",
        )
        self.assertEqual(user.email, "CaseSensitive@example.test")

    def test_display_name_uses_full_name(self):
        self.assertEqual(self.staff_user.display_name, "Maya Patel")
        self.assertEqual(str(self.staff_user), "Maya Patel")

    def test_display_name_falls_back_to_email(self):
        user = User.objects.create_user(
            email="unnamed@example.test",
            password="StrongPassword123.",
        )
        self.assertEqual(user.display_name, "unnamed@example.test")

    def test_superuser_requires_permission_flags(self):
        with self.assertRaisesMessage(ValueError, "is_staff=True"):
            User.objects.create_superuser(
                email="admin@example.test",
                password="StrongPassword123.",
                is_staff=False,
            )
        with self.assertRaisesMessage(ValueError, "is_superuser=True"):
            User.objects.create_superuser(
                email="admin@example.test",
                password="StrongPassword123.",
                is_superuser=False,
            )


class ProfileAndContentModelTests(FinderTestCase):
    def test_staff_profile_name_and_initials(self):
        self.assertEqual(str(self.staff_profile), "Maya Patel")
        self.assertEqual(self.staff_profile.initials, "MP")

    def test_initials_fall_back_to_email(self):
        user = User.objects.create_user(
            email="fallback@example.test",
            password="StrongPassword123.",
        )
        profile = StaffProfile.objects.create(user=user, biography="Fictional.")
        self.assertEqual(profile.initials, "F")

    def test_interest_clean_trims_name(self):
        interest = Interest(staff_profile=self.staff_profile, name="  Accessibility  ")
        interest.full_clean()
        self.assertEqual(interest.name, "Accessibility")

    def test_blank_interest_is_rejected(self):
        interest = Interest(staff_profile=self.staff_profile, name="   ")
        with self.assertRaises(ValidationError):
            interest.full_clean()

    def test_interest_is_case_insensitively_unique_per_owner(self):
        with self.assertRaises(ValidationError):
            Interest(
                staff_profile=self.staff_profile,
                name="DATA ANALYSIS",
            ).full_clean()

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Interest.objects.create(
                    staff_profile=self.staff_profile,
                    name="DATA ANALYSIS",
                )

    def test_same_interest_name_is_allowed_for_different_staff(self):
        interest = Interest(
            staff_profile=self.other_staff_profile,
            name="Data analysis",
        )
        interest.full_clean()

    def test_project_clean_trims_required_text(self):
        project = ProjectIdea(
            staff_profile=self.staff_profile,
            title="  New project  ",
            description="  A sufficiently clear fictional project description.  ",
        )
        project.full_clean()
        self.assertEqual(project.title, "New project")
        self.assertEqual(
            project.description,
            "A sufficiently clear fictional project description.",
        )

    def test_blank_project_fields_are_rejected(self):
        project = ProjectIdea(
            staff_profile=self.staff_profile,
            title=" ",
            description=" ",
        )
        with self.assertRaises(ValidationError) as context:
            project.full_clean()
        self.assertIn("title", context.exception.message_dict)
        self.assertIn("description", context.exception.message_dict)
