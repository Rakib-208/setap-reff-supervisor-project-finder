from time import perf_counter

from django.conf import settings
from django.test import Client
from django.urls import reverse

from finder.models import Interest

from .base import FinderTestCase


class SecurityControlTests(FinderTestCase):
    def test_responses_include_configured_security_headers(self):
        response = self.client.get(reverse("finder:login"))
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["Referrer-Policy"], "same-origin")

    def test_session_cookie_is_http_only_and_same_site(self):
        response = self.client.post(
            reverse("finder:login"),
            {"username": self.student.email, "password": self.student_password},
        )
        session_cookie = response.cookies[settings.SESSION_COOKIE_NAME]
        self.assertTrue(session_cookie["httponly"])
        self.assertEqual(session_cookie["samesite"], "Lax")

    def test_csrf_protection_rejects_untrusted_management_post(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.staff_user)
        response = csrf_client.post(
            reverse("finder:interest-create"),
            {"name": "Untrusted request"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            Interest.objects.filter(
                staff_profile=self.staff_profile,
                name="Untrusted request",
            ).exists()
        )


class NonFunctionalRequirementTests(FinderTestCase):
    def test_directory_response_completes_within_two_seconds(self):
        self.login_student()
        self.client.get(reverse("finder:staff-directory"))

        start = perf_counter()
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"q": "Maya", "interest": "Data analysis"},
        )
        duration = perf_counter() - start

        self.assertEqual(response.status_code, 200)
        self.assertLess(duration, 2.0)

    def test_core_pages_publish_responsive_and_keyboard_landmarks(self):
        login_response = self.client.get(reverse("finder:login"))
        self.assertContains(
            login_response,
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            html=True,
        )
        self.assertContains(login_response, 'class="skip-link"')

        self.login_student()
        directory_response = self.client.get(reverse("finder:staff-directory"))
        self.assertContains(directory_response, 'role="search"')
        self.assertContains(directory_response, 'label for="staff-search"')
        self.assertContains(directory_response, 'label for="interest-filter"')

    def test_invalid_update_preserves_previously_saved_project(self):
        self.login_staff()
        original_title = self.project.title
        original_description = self.project.description

        response = self.client.post(
            reverse("finder:project-update", args=[self.project.pk]),
            {"title": "No", "description": "Too short"},
        )

        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, original_title)
        self.assertEqual(self.project.description, original_description)
