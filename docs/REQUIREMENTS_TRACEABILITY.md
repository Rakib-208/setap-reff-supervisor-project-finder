# Requirements traceability

This table maps the Chapter 1 functional requirements to implementation and
automated evidence. Test files are under `finder/tests/`.

| Requirement | Implementation | Primary automated evidence |
|---|---|---|
| FR01 Authenticate seeded user | Custom email `User`, login form/view, `seed_demo` | `test_authentication.py`, `test_seed_command.py` |
| FR02 Maintain session | Django session middleware and login/logout views | Authentication session/logout tests |
| FR03 Role-specific interface | `access.py`, role-aware home/login redirects | Role redirect and forbidden tests |
| FR04 Log out | POST-only logout view | Logout method/session test |
| FR05 Browse staff directory | `staff_directory` view and directory template | Directory list test |
| FR06 Partial name search | `Concat` and case-insensitive query | Search partition tests |
| FR07 Filter by interest | Validated interest option and ORM filter | Interest filter tests |
| FR08 Clear filters | Clear link and unfiltered directory route | Directory/no-results tests |
| FR09 View staff details | Prefetched profile detail view/template | Profile content and 404 tests |
| FR10 Staff dashboard | Owner-specific dashboard query/template | Dashboard ownership/content tests |
| FR11 Add interest | `InterestForm` and create view | Interest creation test |
| FR12 Update interest | Owner-constrained update view | Interest update/foreign-owner tests |
| FR13 Confirm/delete interest | GET confirmation and POST deletion | Interest confirmation/delete tests |
| FR14 Add project idea | `ProjectIdeaForm` and create view | Project creation/input tests |
| FR15 Update project idea | Owner-constrained update view | Project update/foreign-owner tests |
| FR16 Confirm/delete project | GET confirmation and POST deletion | Project confirmation/delete tests |
| FR17 Validate forms | ModelForm field, length and duplicate rules | Blank/boundary/duplicate partitions |
| FR18 Enforce roles/ownership | Role decorator plus owner-scoped lookups | Student-forbidden and foreign-owner tests |
| FR19 Persist changes | SQLite ORM operations inside atomic blocks | Create/update/delete database assertions |
| FR20 Feedback and empty states | Messages, form errors and empty templates | Validation, no-results and redirect tests |

## Non-functional coverage

| Requirement | Implementation/evidence |
|---|---|
| NFR01 Performance | Small indexed SQLite dataset, related-object prefetching and deterministic queries |
| NFR02 Security | Password hashing, CSRF, session/role/owner checks, safe response headers |
| NFR03 Usability | Visible labels, help text, nearby errors, named deletion and success messages |
| NFR04 Responsive design | Mobile-first breakpoints from 320px upward with no fixed page width |
| NFR05 Reliability | Atomic write operations and validation before persistence |
| NFR06 Compatibility | Standards-based server-rendered HTML and CSS for current Edge/Chrome |
| NFR07 Maintainability | Separate models, forms, access, views, routes, templates and tests |
| NFR08 Data ethics | `.test` emails and clearly labelled fictional seed content |
