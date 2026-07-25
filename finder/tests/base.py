from django.contrib.auth.models import Group
from django.test import TestCase

from finder.models import Interest, ProjectIdea, StaffProfile, User


class FinderTestCase(TestCase):
    student_password = "Student1234."
    staff_password = "Staff1234."

    @classmethod
    def setUpTestData(cls):
        cls.student_group = Group.objects.create(name="Student")
        cls.staff_group = Group.objects.create(name="Staff")

        cls.student = User.objects.create_user(
            email="student@example.test",
            password=cls.student_password,
            first_name="Alex",
            last_name="Morgan",
        )
        cls.student.groups.add(cls.student_group)

        cls.staff_user = User.objects.create_user(
            email="staff@example.test",
            password=cls.staff_password,
            first_name="Maya",
            last_name="Patel",
        )
        cls.staff_user.groups.add(cls.staff_group)
        cls.staff_profile = StaffProfile.objects.create(
            user=cls.staff_user,
            biography="A fictional specialist in data analysis and responsible AI.",
        )
        cls.interest = Interest.objects.create(
            staff_profile=cls.staff_profile,
            name="Data analysis",
        )
        cls.project = ProjectIdea.objects.create(
            staff_profile=cls.staff_profile,
            title="Explainable prediction prototype",
            description=(
                "Build an interpretable prediction prototype with synthetic data."
            ),
        )

        cls.other_staff_user = User.objects.create_user(
            email="other.staff@example.test",
            password="OtherStaff1234.",
            first_name="Liam",
            last_name="Chen",
        )
        cls.other_staff_user.groups.add(cls.staff_group)
        cls.other_staff_profile = StaffProfile.objects.create(
            user=cls.other_staff_user,
            biography="A fictional specialist in graph algorithms.",
        )
        cls.other_interest = Interest.objects.create(
            staff_profile=cls.other_staff_profile,
            name="Graph theory",
        )
        cls.other_project = ProjectIdea.objects.create(
            staff_profile=cls.other_staff_profile,
            title="Network visualisation",
            description="Compare visual layouts for generated network datasets.",
        )

    def login_student(self):
        return self.client.login(
            email=self.student.email,
            password=self.student_password,
        )

    def login_staff(self):
        return self.client.login(
            email=self.staff_user.email,
            password=self.staff_password,
        )
