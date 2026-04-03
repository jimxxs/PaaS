# PaaS Demo — Flask + PostgreSQL on Railway

A minimal REST API built with Python Flask and PostgreSQL, deployed on [Railway](https://railway.app).

## Tech Stack

- Python 3.12 / Flask 3.1
- PostgreSQL (Railway managed)
- SQLAlchemy ORM
- Gunicorn (production server)
- GitHub Actions (CI)

## Project Structure

```
PaaS/
├── app.py                      # Flask app with CRUD routes
├── models.py                   # SQLAlchemy Item model
├── requirements.txt            # Python dependencies
├── Procfile                    # Gunicorn start command
├── railway.toml                # Railway build & deploy config
├── schema.sql                  # DB schema + sample data
├── .env.example                # Environment variable template
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI pipeline
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Health check |
| GET | `/items` | List all items |
| POST | `/items` | Create an item |
| GET | `/items/<id>` | Get a single item |
| PUT | `/items/<id>` | Update an item |
| DELETE | `/items/<id>` | Delete an item |

### Example Requests

```bash
# Create
curl -X POST https://<your-railway-url>/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Dev machine"}'

# List
curl https://<your-railway-url>/items

# Update
curl -X PUT https://<your-railway-url>/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Delete
curl -X DELETE https://<your-railway-url>/items/1
```

## Local Development

### Prerequisites

- Python 3.12+
- A running PostgreSQL instance

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/paas-railway.git
cd paas-railway

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env
# Edit .env and fill in your DATABASE_URL and SECRET_KEY

# 5. Run the app
python app.py
```

The app will be available at `http://localhost:5000`.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Flask secret key |
| `PORT` | Port to bind (set automatically by Railway) |

Never commit `.env`. Use `.env.example` as a reference and set real values in Railway's Variables dashboard.

## Deployment on Railway

1. Push this repo to GitHub.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select this repository — Railway auto-detects Python via Nixpacks.
4. Add a database: **New** → **Database** → **PostgreSQL**. Railway injects `DATABASE_URL` automatically.
5. Add `SECRET_KEY` under your service → **Variables**.
6. Railway deploys automatically. Your public URL appears in the **Settings** tab.

## CI/CD Workflow

Every push to `main`:

1. GitHub Actions runs flake8 lint checks (`.github/workflows/ci.yml`).
2. If checks pass, Railway's GitHub integration triggers an automatic redeployment.

No manual deploy step is needed — Railway watches the `main` branch directly.

## Database Schema

```sql
CREATE TABLE items (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);
```

See [`schema.sql`](schema.sql) for the full schema and sample seed data.

## Scalability Notes

Railway uses usage-based pricing:

| Resource | Rate |
|----------|------|
| vCPU | $0.000463 / vCPU-min |
| RAM | $0.000231 / GB-min |

Scaling plan for increased traffic:

- **Horizontal**: Increase replica count in Railway's service settings.
- **Database**: Upgrade the Railway PostgreSQL plan or migrate to a managed service like AWS RDS.
- **Caching**: Add Redis (available as a Railway plugin) to reduce DB load on read-heavy routes.
- **Rate limiting**: Add Flask-Limiter to protect endpoints from traffic spikes.

## License

MIT
