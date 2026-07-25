# Automated test summary

Verified on 25 July 2026 with Python 3.12.13, Django 6.0.7 and SQLite.

## Result

- Tests discovered: 58
- Tests passed: 58
- Failures/errors: 0
- Assessed-code coverage: 97%
- Django system-check issues: 0

Run the evidence locally:

```powershell
.\.venv\Scripts\python.exe -m coverage erase
.\.venv\Scripts\python.exe -m coverage run manage.py test
.\.venv\Scripts\python.exe -m coverage report -m
```

## Test groups

| Group | Main behaviours covered |
|---|---|
| Models | Email identity, names/initials, trimming, required data and owner-level uniqueness |
| Authentication | Correct/incorrect credentials, supported roles, redirects, sessions and POST logout |
| Directory | Full list, partial/case-insensitive names, valid/invalid interests, combined filters and no results |
| Profiles | Biography, interests, projects, preserved context, missing records and role enforcement |
| Interest management | Create/update/delete, named confirmation, duplicate/blank/boundary inputs and ownership |
| Project management | Create/update/delete, confirmation, length partitions, required fields and ownership |
| Seed command | Exact counts, hashed passwords, correct groups, demo logins, idempotence and unusable extra passwords |
| Quality controls | Security headers, cookie flags, CSRF rejection, response timing, responsive landmarks and rejected-write integrity |

## Partition-testing evidence

The form and search tests deliberately use representative input classes rather
than only happy paths:

- missing, one-character, valid and case-variant duplicate interests;
- missing, below-minimum, valid and above-maximum project titles;
- below-minimum and valid project descriptions;
- matching, non-matching, mixed-case and partial name searches;
- valid, invalid and combined interest/search filters;
- unauthenticated, correct-role, wrong-role and foreign-owner requests;
- GET confirmation, POST mutation and unsupported HTTP methods.

This gives direct evidence for both expected operation and boundary/error
behaviour across the assessed workflows.
