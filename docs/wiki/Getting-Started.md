# Getting Started

## Windows

```powershell
git clone https://github.com/Rakib-208/setap-reff-supervisor-project-finder.git
cd setap-reff-supervisor-project-finder
.\scripts\setup.ps1
.\.venv\Scripts\python.exe manage.py runserver
```

## macOS or Linux

```bash
git clone https://github.com/Rakib-208/setap-reff-supervisor-project-finder.git
cd setap-reff-supervisor-project-finder
./scripts/setup.sh
./.venv/bin/python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Demonstration accounts

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

The credentials are development-only and intentionally public. Each account
has a distinct password, which Django hashes in the local database.
