from django.urls import reverse

from .base import FinderTestCase


class StaffDirectoryTests(FinderTestCase):
    def setUp(self):
        self.login_student()

    def test_directory_lists_all_staff_profiles(self):
        response = self.client.get(reverse("finder:staff-directory"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maya Patel")
        self.assertContains(response, "Liam Chen")
        self.assertEqual(response.context["result_count"], 2)

    def test_name_search_is_case_insensitive_and_partial(self):
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"q": "mAy"},
        )
        self.assertContains(response, "Maya Patel")
        self.assertNotContains(response, "Liam Chen")

    def test_name_search_matches_full_name(self):
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"q": "Maya Pat"},
        )
        self.assertEqual(response.context["result_count"], 1)

    def test_interest_filter_returns_matching_staff(self):
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"interest": "Graph theory"},
        )
        self.assertContains(response, "Liam Chen")
        names = [profile.display_name for profile in response.context["profiles"]]
        self.assertNotIn("Maya Patel", names)

    def test_combined_search_and_filter(self):
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"q": "Liam", "interest": "Graph theory"},
        )
        self.assertEqual(response.context["result_count"], 1)
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"q": "Maya", "interest": "Graph theory"},
        )
        self.assertEqual(response.context["result_count"], 0)

    def test_invalid_interest_filter_is_rejected_clearly(self):
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"interest": "Invented option"},
        )
        self.assertContains(response, "Choose an area of interest")
        self.assertEqual(response.context["selected_interest"], "")

    def test_no_results_state_and_clear_link_are_displayed(self):
        response = self.client.get(
            reverse("finder:staff-directory"),
            {"q": "Nobody"},
        )
        self.assertContains(response, "No matching supervisors")
        self.assertContains(response, "Show all staff")

    def test_profile_contains_biography_interests_and_projects(self):
        response = self.client.get(
            reverse("finder:staff-profile", args=[self.staff_profile.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.staff_profile.biography)
        self.assertContains(response, self.interest.name)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)

    def test_profile_back_link_preserves_search_context(self):
        response = self.client.get(
            reverse("finder:staff-profile", args=[self.staff_profile.pk]),
            {"q": "Maya", "interest": "Data analysis"},
        )
        expected = (
            f"{reverse('finder:staff-directory')}?"
            "q=Maya&amp;interest=Data+analysis"
        )
        self.assertContains(response, expected)

    def test_missing_profile_returns_not_found(self):
        response = self.client.get(
            reverse("finder:staff-profile", args=[99999])
        )
        self.assertEqual(response.status_code, 404)

    def test_staff_cannot_open_student_profile_route(self):
        self.client.logout()
        self.login_staff()
        response = self.client.get(
            reverse("finder:staff-profile", args=[self.staff_profile.pk])
        )
        self.assertEqual(response.status_code, 403)
