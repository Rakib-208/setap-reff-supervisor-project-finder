# Contribution workflow

This assessed individual project uses a lightweight traceable workflow:

1. Start work from a GitHub issue.
2. Create a short-lived `feature/...` branch.
3. Make a focused commit with a descriptive message.
4. Run Django checks and the relevant automated tests.
5. Open a pull request describing requirements and evidence.
6. Merge only after local verification and close the linked issue.

Changes should preserve role enforcement, owner-constrained writes, fictional
data and the separation between models, forms/views and templates.
