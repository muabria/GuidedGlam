# Makeup Website

React frontend (Vite) with a Django backend.

```
.
├── backend/     Django API, admin panel, database models (Python)
├── client/      React app (JavaScript)
├── index.html   Page the React app loads into
└── vite.config.js
```

## Getting started

Backend, first time only (details in [backend/README.md](backend/README.md)):

```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py createsuperuser
```

Frontend, first time only:

```
npm install
```

## Running locally

Run these in two terminals:

```
cd backend && source .venv/bin/activate && python manage.py runserver
```

```
npm run dev
```

- Site: http://localhost:5173 (calls to `/api` and `/auth` are forwarded to Django)
- Admin panel: http://localhost:8000/admin/

## Tests

```
cd backend && python manage.py test
```
