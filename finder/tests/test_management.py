from django.urls import reverse

from finder.models import Interest, ProjectIdea

from .base import FinderTestCase


class StaffDashboardTests(FinderTestCase):
    def setUp(self):
        self.login_staff()

    def test_dashboard_shows_only_authenticated_staff_content(self):
        response = self.client.get(reverse("finder:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.interest.name)
        self.assertContains(response, self.project.title)
        self.assertNotContains(response, self.other_interest.name)
        self.assertNotContains(response, self.other_project.title)

    def test_staff_without_profile_receives_not_found(self):
        self.staff_profile.delete()
        self.assertEqual(self.client.get(reverse("finder:dashboard")).status_code, 404)

    def test_student_is_forbidden_from_every_management_route(self):
        self.client.logout()
        self.login_student()
        urls = [
            reverse("finder:dashboard"),
            reverse("finder:interest-create"),
            reverse("finder:interest-update", args=[self.interest.pk]),
            reverse("finder:interest-delete", args=[self.interest.pk]),
            reverse("finder:project-create"),
            reverse("finder:project-update", args=[self.project.pk]),
            reverse("finder:project-delete", args=[self.project.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)


class InterestManagementTests(FinderTestCase):
    def setUp(self):
        self.login_staff()

    def test_create_interest_persists_owned_record(self):
        response = self.client.post(
            reverse("finder:interest-create"),
            {"name": "Accessibility"},
        )
        self.assertRedirects(response, reverse("finder:dashboard"))
        self.assertTrue(
            Interest.objects.filter(
                staff_profile=self.staff_profile,
                name="Accessibility",
            ).exists()
        )

    def test_create_interest_rejects_blank_short_and_duplicate_values(self):
        cases = [
            ("", "This field is required"),
            ("A", "at least two characters"),
            ("DATA ANALYSIS", "already on your profile"),
        ]
        for value, message in cases:
            with self.subTest(value=value):
                response = self.client.post(
                    reverse("finder:interest-create"),
                    {"name": value},
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, message)
        self.assertEqual(
            Interest.objects.filter(staff_profile=self.staff_profile).count(),
            1,
        )

    def test_update_interest_persists_change(self):
        response = self.client.post(
            reverse("finder:interest-update", args=[self.interest.pk]),
            {"name": "Responsible data analysis"},
        )
        self.assertRedirects(response, reverse("finder:dashboard"))
        self.interest.refresh_from_db()
        self.assertEqual(self.interest.name, "Responsible data analysis")

    def test_delete_interest_requires_confirmation_then_removes_record(self):
        url = reverse("finder:interest-delete", args=[self.interest.pk])
        response = self.client.get(url)
        self.assertContains(response, "Confirmation required")
        self.assertContains(response, self.interest.name)
        self.assertTrue(Interest.objects.filter(pk=self.interest.pk).exists())

        response = self.client.post(url)
        self.assertRedirects(response, reverse("finder:dashboard"))
        self.assertFalse(Interest.objects.filter(pk=self.interest.pk).exists())

    def test_staff_cannot_update_or_delete_foreign_interest(self):
        update_url = reverse(
            "finder:interest-update",
            args=[self.other_interest.pk],
        )
        delete_url = reverse(
            "finder:interest-delete",
            args=[self.other_interest.pk],
        )
        self.assertEqual(
            self.client.post(update_url, {"name": "Stolen"}).status_code,
            404,
        )
        self.assertEqual(self.client.post(delete_url).status_code, 404)
        self.assertTrue(Interest.objects.filter(pk=self.other_interest.pk).exists())

    def test_interest_endpoints_reject_unsupported_method(self):
        self.assertEqual(
            self.client.put(reverse("finder:interest-create")).status_code,
            405,
        )


class ProjectManagementTests(FinderTestCase):
    valid_project = {
        "title": "Accessible feedback assistant",
        "description": (
            "Build a prototype that explains accessibility issues in plain language."
        ),
    }

    def setUp(self):
        self.login_staff()

    def test_create_project_persists_owned_record(self):
        response = self.client.post(
            reverse("finder:project-create"),
            self.valid_project,
        )
        self.assertRedirects(response, reverse("finder:dashboard"))
        self.assertTrue(
            ProjectIdea.objects.filter(
                staff_profile=self.staff_profile,
                title=self.valid_project["title"],
            ).exists()
        )

    def test_create_project_rejects_input_partitions(self):
        cases = [
            (
                {"title": "", "description": self.valid_project["description"]},
                "This field is required",
            ),
            (
                {"title": "Abc", "description": self.valid_project["description"]},
                "at least four characters",
            ),
            (
                {"title": self.valid_project["title"], "description": "Too short"},
                "at least 20 characters",
            ),
            (
                {
                    "title": "X" * 121,
                    "description": self.valid_project["description"],
                },
                "at most 120 characters",
            ),
        ]
        for data, message in cases:
            with self.subTest(data=data):
                response = self.client.post(
                    reverse("finder:project-create"),
                    data,
                )
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, message)

    def test_update_project_persists_both_fields(self):
        response = self.client.post(
            reverse("finder:project-update", args=[self.project.pk]),
            {
                "title": "Updated explainable prototype",
                "description": (
                    "Create and evaluate a revised interpretable prediction tool."
                ),
            },
        )
        self.assertRedirects(response, reverse("finder:dashboard"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated explainable prototype")
        self.assertIn("revised", self.project.description)

    def test_delete_project_requires_confirmation_then_removes_record(self):
        url = reverse("finder:project-delete", args=[self.project.pk])
        response = self.client.get(url)
        self.assertContains(response, "This action cannot be undone")
        self.assertTrue(ProjectIdea.objects.filter(pk=self.project.pk).exists())
        response = self.client.post(url)
        self.assertRedirects(response, reverse("finder:dashboard"))
        self.assertFalse(ProjectIdea.objects.filter(pk=self.project.pk).exists())

    def test_staff_cannot_update_or_delete_foreign_project(self):
        update_url = reverse(
            "finder:project-update",
            args=[self.other_project.pk],
        )
        delete_url = reverse(
            "finder:project-delete",
            args=[self.other_project.pk],
        )
        self.assertEqual(
            self.client.post(update_url, self.valid_project).status_code,
            404,
        )
        self.assertEqual(self.client.post(delete_url).status_code, 404)
        self.assertTrue(ProjectIdea.objects.filter(pk=self.other_project.pk).exists())

    def test_project_endpoints_reject_unsupported_method(self):
        self.assertEqual(
            self.client.patch(reverse("finder:project-create")).status_code,
            405,
        )
