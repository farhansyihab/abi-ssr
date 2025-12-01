# Wagtail CMS - Deployment Guide for Supabase & Google Cloud Run

## 📋 Project Overview

Website built with **Wagtail CMS** deployed on **Google Cloud Run** with **Supabase PostgreSQL**. This setup provides a cost-effective, scalable solution for hosting Wagtail websites.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Google        │    │   Wagtail CMS    │    │   Supabase      │
│   Cloud Run     │────│   (Docker)       │────│   PostgreSQL    │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
abi-site/
├── mysite/                 # Django/Wagtail project
│   ├── settings/
│   │   ├── base.py        # Base settings
│   │   ├── dev.py         # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py
│   └── wsgi.py
├── home/                   # Home app
├── search/                 # Search app
├── Dockerfile             # Production container
├── docker-compose.yml     # Local development
├── requirements.txt       # Python dependencies
├── .env                   # Development environment
├── .env.production        # Production environment
└── manage.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clone and Setup

```bash
# Clone the project
git clone <repository-url>
cd abi-site

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

**Development (.env):**
```bash
DEBUG=True
SECRET_KEY=your-development-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Create the file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### 4. Run Development Server

```bash
# Option 1: Direct Python
python manage.py runserver

# Option 2: Docker Compose
docker-compose up

# Access the site:
# Website: http://localhost:8000
# Admin:   http://localhost:8000/admin
```

## 🐳 Docker Development

### Build and Run with Docker

```bash
# Build image
docker build -t abi-site .

# Run container
docker run -p 8000:8000 --env-file .env abi-site

# Or use docker-compose
docker-compose up --build
```

### Docker Compose for Development

The `docker-compose.yml` file is configured for local development with:
- Hot reloading for code changes
- Environment variables from `.env`
- Port 8000 exposed

## ☁️ Production Deployment

### 1. Supabase Setup

1. **Create Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note: Project URL, Password, Database details

2. **Get Connection String**
   ```
   postgresql://postgres:your-password@db.your-project-ref.supabase.co:5432/postgres
   ```

### 2. Google Cloud Setup

1. **Install Google Cloud SDK**
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable \
     run.googleapis.com \
     containerregistry.googleapis.com \
     cloudbuild.googleapis.com
   ```

### 3. Production Environment

Update `.env.production`:
```bash
DEBUG=False
SECRET_KEY=your-very-secure-production-secret-key
DATABASE_URL=postgresql://postgres:your-password@db.your-ref.supabase.co:5432/postgres
ALLOWED_HOSTS=your-service.a.run.app,your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-service.a.run.app,https://your-domain.com
```

### 4. Deployment Commands

```bash
# Set your project ID
export GCP_PROJECT="your-project-id"
export SERVICE_NAME="abi-site"

# Build and push to Container Registry
docker build -t gcr.io/$GCP_PROJECT/$SERVICE_NAME .
docker push gcr.io/$GCP_PROJECT/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$GCP_PROJECT/$SERVICE_NAME \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --set-env-vars "DATABASE_URL=postgresql://..." \
  --set-env-vars "SECRET_KEY=..." \
  --set-env-vars "ALLOWED_HOSTS=your-service.a.run.app" \
  --set-env-vars "DEBUG=False"
```

## 🔧 Configuration

### Wagtail Settings

The project uses a modular settings structure:

- **`mysite/settings/base.py`** - Common settings
- **`mysite/settings/dev.py`** - Development-specific
- **`mysite/settings/production.py`** - Production-specific

### Environment Variables

| Variable | Development | Production |
|----------|-------------|------------|
| `DEBUG` | `True` | `False` |
| `DATABASE_URL` | SQLite | Supabase PostgreSQL |
| `ALLOWED_HOSTS` | localhost | your-domain.com |
| `SECRET_KEY` | Development key | Secure random key |

## 📊 Database Management

### Local Development
```bash
# SQLite database (default for development)
python manage.py migrate
python manage.py createsuperuser
```

### Production (Supabase)
```bash
# Run migrations on production
docker run --env-file .env.production your-image python manage.py migrate

# Create superuser on production
docker run --env-file .env.production -it your-image python manage.py createsuperuser
```

## 🛠️ Maintenance

### Backup Database
```bash
# Supabase provides automatic backups
# Manual backup through Supabase dashboard
```

### Logs and Monitoring
```bash
# View Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit=20

# Check service status
gcloud run services describe $SERVICE_NAME --region asia-southeast2
```

### Update Deployment
```bash
# Rebuild and redeploy
docker build -t gcr.io/$GCP_PROJECT/$SERVICE_NAME .
docker push gcr.io/$GCP_PROJECT/$SERVICE_NAME
gcloud run deploy $SERVICE_NAME --image gcr.io/$GCP_PROJECT/$SERVICE_NAME
```

## 🔒 Security Notes

- Never commit `.env` or `.env.production` files
- Use strong secret keys in production
- Enable SSL/HTTPS in production
- Regularly update dependencies
- Monitor Supabase usage and costs

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check Supabase connection string
   - Verify database is running
   - Check network connectivity

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check Whitenoise configuration
   - Verify Cloud Run storage permissions

3. **Migration Errors**
   - Ensure all migrations are applied
   - Check database compatibility
   - Verify model changes

### Getting Help

- Check Cloud Run logs: `gcloud logging read`
- Verify Supabase connection
- Test locally before deploying

## 📝 Useful Commands

### Development
```bash
# Run tests
python manage.py test

# Create new migration
python manage.py makemigrations

# Check project health
python manage.py check --deploy
```

### Production
```bash
# Scale service
gcloud run services update $SERVICE_NAME --concurrency 80 --cpu 1 --memory 512Mi

# Custom domain
gcloud run domain-mappings create --service $SERVICE_NAME --domain your-domain.com
```

## 💰 Cost Optimization

- Supabase: Free tier available
- Cloud Run: Pay-per-use pricing
- Monitor usage in Google Cloud Console
- Set budget alerts

---

## 📞 Support

For issues with:
- **Wagtail CMS**: [Wagtail Documentation](https://docs.wagtail.org)
- **Google Cloud Run**: [Google Cloud Documentation](https://cloud.google.com/run/docs)
- **Supabase**: [Supabase Documentation](https://supabase.com/docs)

---

**Happy Coding!** 🚀