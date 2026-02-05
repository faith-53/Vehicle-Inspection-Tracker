## Vehicle Inspection Tracker (Django)

This project is a simple Vehicle Inspection Tracker built with Django. It provides:

- REST API to create, list, retrieve, and update inspections.
- Business rules enforcing valid statuses and future inspection dates.
- Two automated tests covering successful creation and past-date rejection.
- Optional web UI for scheduling inspections and viewing all records.

### Requirements

- Python 3.11+ (or compatible with your Django installation)
- pip

All Python dependencies are installed into a local virtual environment.

### Setup & Run Instructions

1. Clone or open the project directory

   Ensure your shell is at:

   ```bash
   cd "C:\\Users\\user\\Desktop\\Vehicle Inspection Tracker"
   ```

2. Create and activate virtual environment (if not already active)

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install django
   ```

4. Apply migrations

   ```bash
   python manage.py migrate
   ```

5. Run the development server

   ```bash
   python manage.py runserver
   ```

6. Access the application

   - Web UI (optional): `http://127.0.0.1:8000/`
   - API endpoints:
     - `POST /api/inspections` – create new inspection
     - `GET /api/inspections` – list all inspections
     - `GET /api/inspections/{id}` – get single inspection
     - `PUT /api/inspections/{id}` – update existing inspection

### Data Model

The single model is `Inspection` with these exact fields:

- vehicle_plate (`string`, required) – e.g. `"ABC-1234"`
- inspection_date (`date`, required) – e.g. `"2024-12-25"`
- status (`string`, required) – exactly one of `"scheduled"`, `"passed"`, `"failed"`
- notes (`string`, optional) – e.g. `"Brakes need servicing"`

Validation rules:

- No past dates: `inspection_date` must be today or in the future.
- Strict status values: `status` must be one of `"scheduled"`, `"passed"`, `"failed"`.

Both the API layer and the model validation enforce these rules.

### Running Tests

The project includes exactly two automated tests:

1. Successful inspection creation with valid data.
2. Rejection of inspections with past dates.

Run them with:

```bash
python manage.py test inspections
```

### Notable Implementation Details

- API implementation uses simple function-based views in `inspections/views.py` handling JSON manually via `JsonResponse`, without extra libraries.
- Endpoints:
  - `inspections_collection` handles `GET` (list) and `POST` (create).
  - `inspection_detail` handles `GET` (retrieve) and `PUT` (update).
- Frontend (`templates/inspections/index.html`) uses a basic HTML form and JavaScript `fetch` calls to the same API.

### Challenges Encountered

- Date validation for past inspections: To ensure consistency across environments and avoid timezone issues, the implementation uses Django's `timezone.localdate()` when comparing `inspection_date` values.
- Keeping validation DRY: Both the model and the API enforce the same business rules (allowed statuses and no past dates). To keep things clear for this exercise, the rules are explicitly checked in the API views so that clients receive straightforward JSON error messages, while the model still has `clean()` for additional safety.
- PowerShell command chaining: While setting up locally on Windows, `&&` could not be used as a command separator in some environments. Commands were instead run on separate lines or as separate invocations to avoid shell parsing issues.

