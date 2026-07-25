# Implementation architecture

ProjectFinder is a self-contained, server-rendered Django application. The
implementation follows the layered Model-View-Template structure specified in
Chapter 2 while keeping the prototype small enough to run locally with SQLite.

## System boundary

The application contains:

- seeded local authentication;
- Student and Staff role authorisation;
- a staff directory and staff profile viewer;
- protected staff management for interests and project ideas;
- SQLite persistence and automated tests.

It intentionally excludes registration, real University identity, supervisor
allocation, student records, messaging, uploads and production hosting.

## Layer mapping

| Layer | Repository components | Responsibility |
|---|---|---|
| Presentation | `templates/`, `finder/static/` | Semantic HTML, responsive layout, forms, messages and empty states |
| Routing | `config/urls.py`, `finder/urls.py` | Stable URL-to-view mapping |
| Request coordination | `finder/views.py` | Role checks, ORM queries, validation flow, transactions and redirects |
| Validation/access policy | `finder/forms.py`, `finder/access.py` | Input boundaries, group membership and protected-view decorators |
| Domain/data access | `finder/models.py`, Django ORM | Users, profiles, interests, ideas, ownership and persistence |
| Persistence | `db.sqlite3` locally | Demonstration records, sessions and Django metadata |

## Student request lifecycle

1. Django session middleware resolves the authenticated custom `User`.
2. `role_required("Student")` rejects unauthenticated or wrong-role requests.
3. The directory view builds a deterministic `StaffProfile` query.
4. A name query is trimmed and applied as a case-insensitive partial match.
5. An interest value is checked against stored filter options before use.
6. Related interests are prefetched and project totals are annotated.
7. The template displays result cards or a meaningful no-results state.

Profile requests follow the same role boundary and prefetch the selected
profile's interests and project ideas before rendering a read-only page.

## Staff mutation lifecycle

1. The request must belong to the Staff group.
2. The application resolves the `StaffProfile` belonging to the current user.
3. Update/delete records are looked up using both primary key and that profile.
4. A `ModelForm` validates required values, length rules and duplicates.
5. Successful writes run inside `transaction.atomic()`.
6. Django redirects to the dashboard and displays operation feedback.

The owner-constrained lookup is the important security boundary. Hiding an Edit
button is not treated as authorisation; a crafted URL for another owner's record
returns `404` without revealing or changing that record.

## Identity and role model

Both roles use one custom `User` model with unique email authentication.
Django groups distinguish Student and Staff access:

- Student users need no extra stored attributes for the assessed workflows.
- Staff users have one `StaffProfile` containing a biography.
- `Interest` and `ProjectIdea` each reference exactly one `StaffProfile`.

This avoids duplicating authentication data in separate Student and Staff
models. A `StudentProfile` can be introduced later only if genuine student
attributes become necessary.

## Data integrity and indexes

- Email is unique.
- Staff profile ownership is one-to-one.
- Interest names are case-insensitively unique per staff profile.
- Required project fields are length-limited and trimmed.
- Foreign keys cascade when their owning staff profile is deleted.
- Composite indexes support deterministic user display and owner/content order.

## Security controls

- Django password hashing; no plaintext password comparisons.
- CSRF middleware and tokens on unsafe forms.
- HTTP-only, SameSite session cookies.
- Student/Staff role decorators on protected views.
- Owner-scoped ORM lookups on every staff mutation.
- POST-only logout and GET/POST restrictions on management views.
- `nosniff`, frame-denial and same-origin referrer headers.
- Clearly fictional `.test` accounts and project content.

## Key decisions

### Server-rendered monolith

A separate JavaScript frontend/API would duplicate validation and increase
authentication, cross-origin and deployment work without improving the required
directory and form workflows. Django templates provide the needed interactivity
with a smaller failure surface.

### SQLite for the prototype

SQLite keeps setup reproducible and needs no external service. It is suitable
for assessment demonstration and automated tests, but concurrent institutional
deployment would require a database and operations review.

### Seeded accounts instead of registration

The brief requires staff maintenance and student browsing, not public account
creation. Seeded users make the demonstration repeatable and prevent registration
from consuming implementation time without adding assessed value.

## Evidence links

- `docs/REQUIREMENTS_TRACEABILITY.md` maps FR01-FR20 to code and tests.
- `docs/TEST_SUMMARY.md` records the verified automated evidence.
- `docs/DEMO_SCRIPT.md` provides the timed assessment walkthrough.
