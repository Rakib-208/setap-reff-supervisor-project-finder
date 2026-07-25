# Implementation Architecture

ProjectFinder uses a layered Django Model-View-Template structure:

| Concern | Main location |
|---|---|
| Routes | `config/urls.py`, `finder/urls.py` |
| Request and workflow logic | `finder/views.py` |
| Validation | `finder/forms.py` |
| Role policy | `finder/access.py` |
| Domain and persistence | `finder/models.py` |
| Presentation | `templates/`, `finder/static/` |
| Automated evidence | `finder/tests/` |

One custom email `User` supports both roles. Student and Staff Django groups
control route access. Staff users additionally own one `StaffProfile`; its
`Interest` and `ProjectIdea` records are always retrieved through the
authenticated owner for mutation.

The full design rationale and request lifecycles are maintained in
[docs/ARCHITECTURE.md](https://github.com/Rakib-208/setap-reff-supervisor-project-finder/blob/main/docs/ARCHITECTURE.md).
