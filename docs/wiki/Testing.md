# Testing

Run every automated check on Windows:

```powershell
.\scripts\verify.ps1
```

Or on macOS/Linux:

```bash
./scripts/verify.sh
```

The verification covers:

- Django configuration and migration drift;
- authentication and sessions;
- Student and Staff route separation;
- directory search/filter input partitions;
- complete interest and project management;
- validation and rejected writes;
- foreign-owner attacks;
- security headers, cookies and CSRF;
- response timing and responsive landmarks;
- repeatable fictional seed data.

The verified result for release 1.0.0 is 59 passing tests and 97% assessed-code
coverage. Detailed partitions are recorded in
[docs/TEST_SUMMARY.md](https://github.com/Rakib-208/setap-reff-supervisor-project-finder/blob/main/docs/TEST_SUMMARY.md).
