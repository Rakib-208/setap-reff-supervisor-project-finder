# Security and prototype boundary

ProjectFinder is an academic demonstration and must not be used with real
student, staff or University data.

Implemented controls include Django password hashing, CSRF middleware,
HTTP-only session cookies, role checks, owner-constrained queries, atomic writes,
safe response headers and server-side validation.

The published seed passwords are development-only credentials. Before any
non-local deployment, replace the secret key, disable debug mode, use HTTPS,
review allowed hosts and cookies, replace SQLite where appropriate, rotate all
accounts and complete institutional security/data-protection assessment.

For repository security concerns, open a private communication channel with
the repository owner rather than publishing real credentials or personal data
in an issue.
