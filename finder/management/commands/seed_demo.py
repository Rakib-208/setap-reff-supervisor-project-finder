from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from finder.demo_accounts import STAFF_ACCOUNTS, STUDENT_ACCOUNTS
from finder.models import Interest, ProjectIdea, StaffProfile, User


STAFF_RECORDS = [
    {
        "email": "staff@example.test",
        "first_name": "Maya",
        "last_name": "Patel",
        "biography": (
            "Maya explores practical approaches to trustworthy data analysis and "
            "machine learning. Her fictional supervision examples focus on clear "
            "evaluation, responsible data use and useful prototypes."
        ),
        "interests": ["Data analysis", "Machine learning", "Responsible AI"],
        "projects": [
            (
                "Explaining student-success predictions",
                "Build and evaluate an interpretable classification prototype using "
                "a fully synthetic student dataset. Compare predictive performance "
                "with the clarity of the resulting explanations.",
            ),
            (
                "Responsible dataset quality checker",
                "Develop a web tool that identifies missing values, imbalance and "
                "possible data-quality risks before a dataset is used for analysis.",
            ),
        ],
    },
    {
        "email": "daniel.okoro@example.test",
        "first_name": "Daniel",
        "last_name": "Okoro",
        "biography": (
            "Daniel's fictional profile covers software evolution, program analysis "
            "and dependable delivery practices for maintainable systems."
        ),
        "interests": ["DevOps", "Program analysis", "Software maintenance"],
        "projects": [
            (
                "Repository maintainability dashboard",
                "Create a dashboard that summarises code churn, issue activity and "
                "maintenance indicators for an open-source repository.",
            ),
            (
                "Automated technical-debt triage",
                "Investigate simple rules for grouping and prioritising maintenance "
                "tasks extracted from a synthetic issue dataset.",
            ),
        ],
    },
    {
        "email": "sofia.bennett@example.test",
        "first_name": "Sofia",
        "last_name": "Bennett",
        "biography": (
            "Sofia's fictional work considers inclusive interaction design, "
            "accessibility evaluation and evidence-led improvements to user journeys."
        ),
        "interests": ["Accessibility", "Human-computer interaction", "UX research"],
        "projects": [
            (
                "Accessible campus navigation study",
                "Prototype and evaluate an accessible journey-planning interface "
                "using fictional campus locations and representative user tasks.",
            ),
            (
                "Plain-language form assistant",
                "Design a tool that helps authors identify unclear instructions and "
                "improve the usability of complex online forms.",
            ),
        ],
    },
    {
        "email": "liam.chen@example.test",
        "first_name": "Liam",
        "last_name": "Chen",
        "biography": (
            "Liam's fictional research interests connect graph models, practical "
            "algorithms and the analysis of networks."
        ),
        "interests": ["Algorithms", "Graph theory", "Network science"],
        "projects": [
            (
                "Visual route-planning algorithm explorer",
                "Build an interactive comparison of shortest-path algorithms using "
                "small generated networks and clearly reported performance measures.",
            ),
            (
                "Community detection in synthetic networks",
                "Compare community-detection techniques on generated social-network "
                "graphs without collecting personal data.",
            ),
        ],
    },
    {
        "email": "aisha.rahman@example.test",
        "first_name": "Aisha",
        "last_name": "Rahman",
        "biography": (
            "Aisha's fictional profile focuses on usable cyber security, privacy "
            "engineering and introductory digital-forensics workflows."
        ),
        "interests": ["Cyber security", "Digital forensics", "Privacy engineering"],
        "projects": [
            (
                "Phishing-awareness feedback tool",
                "Develop a safe training prototype that explains suspicious features "
                "in fictional messages and records no personal information.",
            ),
            (
                "Privacy review checklist assistant",
                "Create a guided checklist that helps small software projects identify "
                "common privacy risks and document proportionate mitigations.",
            ),
        ],
    },
]


class Command(BaseCommand):
    help = "Create or refresh fictional demonstration users and staff content."

    @transaction.atomic
    def handle(self, *args, **options):
        student_group, _ = Group.objects.get_or_create(name="Student")
        staff_group, _ = Group.objects.get_or_create(name="Staff")

        for record in STUDENT_ACCOUNTS:
            student, _ = User.objects.update_or_create(
                email=record["email"],
                defaults={
                    "first_name": record["first_name"],
                    "last_name": record["last_name"],
                    "is_active": True,
                },
            )
            student.set_password(record["password"])
            student.save(update_fields=["password"])
            student.groups.set([student_group])

        staff_passwords = {
            account["email"]: account["password"] for account in STAFF_ACCOUNTS
        }
        for record in STAFF_RECORDS:
            user, _ = User.objects.update_or_create(
                email=record["email"],
                defaults={
                    "first_name": record["first_name"],
                    "last_name": record["last_name"],
                    "is_active": True,
                },
            )
            user.set_password(staff_passwords[record["email"]])
            user.save(update_fields=["password"])
            user.groups.set([staff_group])

            profile, _ = StaffProfile.objects.update_or_create(
                user=user,
                defaults={"biography": record["biography"]},
            )
            Interest.objects.filter(staff_profile=profile).delete()
            ProjectIdea.objects.filter(staff_profile=profile).delete()
            Interest.objects.bulk_create(
                [
                    Interest(staff_profile=profile, name=name)
                    for name in record["interests"]
                ]
            )
            ProjectIdea.objects.bulk_create(
                [
                    ProjectIdea(
                        staff_profile=profile,
                        title=title,
                        description=description,
                    )
                    for title, description in record["projects"]
                ]
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Created fictional demo data: 3 students, 5 staff profiles, "
                "15 interests and 10 project ideas."
            )
        )
