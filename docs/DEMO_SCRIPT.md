# 3-5 minute demonstration script

Target duration: approximately 4 minutes.

Before recording:

1. Run migrations and `seed_demo`.
2. Open the application at `http://127.0.0.1:8000/`.
3. Use a clean browser window at a desktop width.
4. Keep the GitHub repository ready in a second tab for the closing evidence.

## 0:00-0:30 - Introduce the problem

Explain that final-year students need a simple way to compare potential
supervisors, expertise and project ideas. State that all displayed information
is fictional and that the prototype has separate Student and Staff roles.

Show the login page and point out the clearly published demonstration accounts.

## 0:30-1:35 - Student discovery

1. Sign in with `student@example.test` and `Student1234.`.
2. Show the complete directory and responsive staff cards.
3. Search for `Maya` to demonstrate case-insensitive partial-name matching.
4. Clear the search, then filter by `Graph theory`.
5. Choose a profile and show its biography, interest tags and project ideas.
6. Use the back link to return to the preserved directory context.
7. Briefly demonstrate a no-results state with an impossible name.

## 1:35-3:20 - Staff content management

1. Sign out and sign in with `staff@example.test` and `Staff1234.`.
2. Show the owner-specific dashboard and content totals.
3. Add the interest `Information visualisation`.
4. Edit it to `Data visualisation`.
5. Attempt to add `DATA VISUALISATION` again to show duplicate validation.
6. Add a project:
   - Title: `Accessible data dashboard`
   - Description: `Design and evaluate a dashboard that presents complex data with accessible summaries.`
7. Edit the project title to `Inclusive data dashboard`.
8. Open its Delete action, point out the named confirmation and cancel.
9. Re-open Delete and confirm, showing the success feedback and persisted result.

## 3:20-4:00 - Engineering evidence

Open the public GitHub repository and briefly show:

- the small commit history and merged feature branches/pull requests;
- the four tracked implementation issues;
- the separated `models.py`, `views.py`, `forms.py` and templates;
- the automated test folders;
- the README test result: 52 passing tests and 97% coverage.

Finish by restating that the prototype implements student discovery, protected
staff maintenance, validation, ownership and persistence.

## Recording reminder

Upload the recording to an accessible video service and add only its sharing
link to Chapter 3. Check the link in a signed-out/private browser window before
submission.
