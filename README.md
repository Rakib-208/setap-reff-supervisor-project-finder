# ProjectFinder

[![Django verification](https://github.com/Rakib-208/setap-reff-supervisor-project-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/Rakib-208/setap-reff-supervisor-project-finder/actions/workflows/ci.yml)

ProjectFinder is a Django prototype for final-year project discovery. Students
can search fictional academic profiles, filter by specialist interest and
review proposed projects. Staff can securely maintain only the interests and
project ideas attached to their own profile.

This repository supports the Software Engineering Theory and Practice
(M30819) referral project. All people, accounts and project content are
fictional demonstration data.

## Implemented functionality

### Student

- Sign in with a seeded student account.
- Browse all staff profiles.
- Search staff with a case-insensitive partial name.
- Filter staff by an available area of interest.
- Combine and clear search criteria.
- View a profile containing a biography, interests and project ideas.
- Receive clear empty, validation and access-denied states.

### Staff

- Sign in and reach an owner-specific dashboard.
- Add, edit and delete areas of interest.
- Add, edit and delete project ideas.
- Review a named confirmation page before deletion.
- Receive validation and operation feedback.
- Remain unable to change another staff member's content.

### Quality and security

- Email-based Django authentication with hashed passwords.
- Server-side Student and Staff role checks.
- Owner-constrained database queries for every management operation.
- CSRF protection on state-changing forms.
- Atomic create, update and delete operations.
- Responsive layouts from small mobile to desktop widths.
- Keyboard focus styles, semantic headings, labels and skip navigation.
- 59 automated tests with 97% statement/branch coverage of assessed code.

## Demonstration accounts

Run the seed command before using these accounts.

| Role | Email | Password |
|---|---|---|
| Student - Alex Morgan | `student@example.test` | `AlexStudent1234.` |
| Student - Jordan Lee | `jordan.lee@example.test` | `JordanStudent1234.` |
| Student - Taylor Reed | `taylor.reed@example.test` | `TaylorStudent1234.` |
| Staff - Maya Patel | `staff@example.test` | `MayaStaff1234.` |
| Staff - Daniel Okoro | `daniel.okoro@example.test` | `DanielStaff1234.` |
| Staff - Sofia Bennett | `sofia.bennett@example.test` | `SofiaStaff1234.` |
| Staff - Liam Chen | `liam.chen@example.test` | `LiamStaff1234.` |
| Staff - Aisha Rahman | `aisha.rahman@example.test` | `AishaStaff1234.` |

These development-only credentials are intentionally published for assessment
demonstration. Every account has a distinct password, and Django stores those
passwords as salted hashes in SQLite.

## Local setup

The project requires Python 3.12 or later.

For a complete automated setup on Windows, run:

```powershell
.\scripts\setup.ps1
```

On macOS or Linux, run:

```bash
./scripts/setup.sh
```

The equivalent manual commands are shown below for transparency.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py runserver
```

### macOS or Linux

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py seed_demo
./.venv/bin/python manage.py runserver
```

Open `http://127.0.0.1:8000/` and use one of the demonstration accounts.
The `seed_demo` command is repeatable and safely restores the fictional baseline.

## Automated tests

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Alternatively, run `.\scripts\verify.ps1` on Windows or
`./scripts/verify.sh` on macOS/Linux to perform the Django system check,
migration-drift check, complete test suite and 95% minimum coverage check.

Run the tests with coverage:

```powershell
.\.venv\Scripts\python.exe -m coverage erase
.\.venv\Scripts\python.exe -m coverage run manage.py test
.\.venv\Scripts\python.exe -m coverage report -m
```

The latest verified result is **59 passing tests and 97% coverage**. Tests cover
authentication, roles, directory search/filter partitions, profile display,
model rules, validation, staff CRUD, confirmation, ownership attacks, HTTP
methods and repeatable seed data. See `docs/TEST_SUMMARY.md`.

## Main routes

| Route | Role | Purpose |
|---|---|---|
| `/login/` | Signed out | Seeded account login |
| `/staff/` | Student | Browse, search and filter staff |
| `/staff/<id>/` | Student | Read a staff profile |
| `/dashboard/` | Staff | Manage owned profile content |
| `/dashboard/interests/add/` | Staff | Add an interest |
| `/dashboard/interests/<id>/edit/` | Staff owner | Edit an interest |
| `/dashboard/interests/<id>/delete/` | Staff owner | Confirm/delete an interest |
| `/dashboard/projects/add/` | Staff | Add a project idea |
| `/dashboard/projects/<id>/edit/` | Staff owner | Edit a project idea |
| `/dashboard/projects/<id>/delete/` | Staff owner | Confirm/delete a project |

## Project structure

```text
config/                     Django project settings and root routing
finder/
  access.py                 Role checks
  forms.py                  Login and validated content forms
  models.py                 User, profile, interest and project entities
  views.py                  Discovery and staff-management workflows
  management/commands/      Repeatable fictional seed command
  static/                   Responsive application styling
  tests/                    Automated model, view, security and seed tests
templates/                  Accessible server-rendered pages
docs/                       Demo, testing, traceability and AI-use evidence
```

## Documentation

- `CHANGELOG.md` - versioned record of delivered functionality.
- `docs/DEMO_SCRIPT.md` - a timed 3-5 minute assessment demonstration.
- `docs/ARCHITECTURE.md` - implementation layers, request flows and decisions.
- `docs/MAINTENANCE.md` - repeatable operation, changes and troubleshooting.
- `docs/REQUIREMENTS_TRACEABILITY.md` - requirements mapped to code and tests.
- `docs/TEST_SUMMARY.md` - test strategy, partitions and verified result.
- `docs/AI_USE.md` - transparent acknowledgement of AI assistance.
- `SECURITY.md` - prototype security boundary and reporting notes.
- `docs/wiki/` - version-controlled source for the GitHub Wiki pages.

## Release

The completed assessment prototype is versioned as **1.0.0**. The release is
reproducible from migrations plus the `seed_demo` command; the local SQLite
database is intentionally excluded.

## Scope

This is a local academic prototype, not a production University service. It
does not provide registration, supervisor allocation, real University identity,
email, file uploads or student-record integration. SQLite is appropriate for
the reproducible assessment demonstration but would require review for a
concurrent institutional deployment.

## AI acknowledgement

AI tools assisted with planning, implementation, documentation and test
generation. Their output was reviewed, executed and verified against the
assessment requirements. Full details are recorded in `docs/AI_USE.md`.
