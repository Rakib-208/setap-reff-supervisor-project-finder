from django.contrib.auth.models import Group
from django.urls import reverse

from finder.demo_accounts import STAFF_ACCOUNTS, STUDENT_ACCOUNTS
from finder.models import User

from .base import FinderTestCase


class AuthenticationTests(FinderTestCase):
    def test_login_page_displays_every_demo_account(self):
        response = self.client.get(reverse("finder:login"))
        self.assertEqual(response.status_code, 200)
        for account in (*STUDENT_ACCOUNTS, *STAFF_ACCOUNTS):
            with self.subTest(email=account["email"]):
                self.assertContains(response, account["first_name"])
                self.assertContains(response, account["email"])
                self.assertContains(response, account["password"])

    def test_valid_student_login_redirects_to_directory(self):
        response = self.client.post(
            reverse("finder:login"),
            {"username": self.student.email, "password": self.student_password},
        )
        self.assertRedirects(response, reverse("finder:staff-directory"))

    def test_valid_staff_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("finder:login"),
            {"username": self.staff_user.email, "password": self.staff_password},
        )
        self.assertRedirects(response, reverse("finder:dashboard"))

    def test_invalid_credentials_return_plain_language_error(self):
        response = self.client.post(
            reverse("finder:login"),
            {"username": self.student.email, "password": "incorrect"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "email address or password is incorrect")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_account_without_role_is_not_logged_in(self):
        user = User.objects.create_user(
            email="no.role@example.test",
            password="StrongPassword123.",
        )
        response = self.client.post(
            reverse("finder:login"),
            {"username": user.email, "password": "StrongPassword123."},
        )
        self.assertContains(response, "does not have a supported Student or Staff role")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_home_redirects_each_role_to_correct_interface(self):
        self.login_student()
        self.assertRedirects(
            self.client.get(reverse("finder:home")),
            reverse("finder:staff-directory"),
        )
        self.client.logout()
        self.login_staff()
        self.assertRedirects(
            self.client.get(reverse("finder:home")),
            reverse("finder:dashboard"),
        )

    def test_authenticated_login_page_redirects_to_role_home(self):
        self.login_student()
        self.assertRedirects(
            self.client.get(reverse("finder:login")),
            reverse("finder:staff-directory"),
        )

    def test_logout_requires_post_and_invalidates_session(self):
        self.login_student()
        self.assertEqual(self.client.get(reverse("finder:logout")).status_code, 405)
        response = self.client.post(reverse("finder:logout"))
        self.assertRedirects(response, reverse("finder:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unauthenticated_protected_route_redirects_with_next(self):
        url = reverse("finder:staff-directory")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('finder:login')}?next={url}",
        )

    def test_wrong_role_receives_forbidden_response(self):
        self.login_student()
        self.assertEqual(self.client.get(reverse("finder:dashboard")).status_code, 403)
        self.client.logout()
        self.login_staff()
        self.assertEqual(
            self.client.get(reverse("finder:staff-directory")).status_code,
            403,
        )

    def test_user_with_both_groups_uses_student_interface_first(self):
        self.staff_user.groups.add(Group.objects.get(name="Student"))
        self.login_staff()
        self.assertRedirects(
            self.client.get(reverse("finder:home")),
            reverse("finder:staff-directory"),
        )
