# Django backend

Python version of the Express server in `../server`. Same URLs (`/api/...`, `/auth/...`), plus an admin panel at `/admin/`.

## First-time setup

```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate          # create the database tables
python manage.py seed             # face shapes, skin tones, skin types
python manage.py createsuperuser  # your admin login
```

## Day to day

```
python manage.py runserver        # API on http://localhost:8000
npm run dev                       # (from the project root) React on http://localhost:5173
python manage.py test             # run the tests
```

After changing anything in a `models.py`:

```
python manage.py makemigrations
python manage.py migrate
```

## Where things are

| File | What it does |
|---|---|
| `config/settings.py` | Project settings (database, installed apps, token lifetime) |
| `accounts/` | Users: register, login, account, admin-only routes |
| `catalog/models.py` | Makeup products, comments, categories, skin tones, skin types, face shapes |
| `catalog/views.py` | The `/api/...` routes |
| `catalog/admin.py` | What shows up in the admin panel |

It uses a local SQLite file by default. To use Postgres, copy `.env.example` to `.env` and set `DATABASE_URL`.
