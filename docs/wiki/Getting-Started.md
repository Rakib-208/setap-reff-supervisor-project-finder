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
| Student | `student@example.test` | `Student1234.` |
| Staff | `staff@example.test` | `Staff1234.` |

The credentials are development-only and intentionally public. Password values
are hashed by Django in the local database.
