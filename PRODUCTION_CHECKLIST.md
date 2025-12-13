# Farmo Production Deployment Checklist

## Pre-Deployment Security

### 1. Environment Configuration
- [ ] Create `.env` file from `.env.example`
- [ ] Generate strong SECRET_KEY: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] Set `DEBUG=False`
- [ ] Configure production domain in `ALLOWED_HOSTS`
- [ ] Update `CORS_ALLOWED_ORIGINS` with production frontend URL
- [ ] Set strong database password

### 2. Database Security
- [ ] Use PostgreSQL with SSL connection
- [ ] Create database user with limited privileges
- [ ] Enable database connection encryption
- [ ] Regular automated backups configured
- [ ] Restrict database access to application server only

### 3. HTTPS/SSL
- [ ] Obtain SSL certificate (Let's Encrypt recommended)
- [ ] Configure web server (Nginx/Apache) with SSL
- [ ] Force HTTPS redirect
- [ ] Verify `SECURE_SSL_REDIRECT=True`
- [ ] Enable HSTS headers

### 4. Server Configuration
- [ ] Use Gunicorn/uWSGI for production server
- [ ] Configure Nginx as reverse proxy
- [ ] Set up firewall (UFW/iptables)
- [ ] Disable unnecessary ports
- [ ] Configure fail2ban for brute force protection

### 5. Application Security
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Create logs directory: `mkdir logs`
- [ ] Set proper file permissions (644 for files, 755 for directories)
- [ ] Remove development dependencies

### 6. Monitoring & Logging
- [ ] Configure error logging to file
- [ ] Set up security event logging
- [ ] Monitor failed login attempts
- [ ] Configure log rotation
- [ ] Set up uptime monitoring

### 7. Rate Limiting
- [ ] Verify throttling is enabled (100/hour for anonymous, 1000/hour for authenticated)
- [ ] Configure Nginx rate limiting
- [ ] Monitor API abuse

### 8. JWT Token Security
- [ ] Tokens transmitted over HTTPS only
- [ ] Access token lifetime: 1 hour
- [ ] Refresh token lifetime: 7 days
- [ ] Token rotation enabled

### 9. Password & PIN Security
- [ ] All passwords hashed with PBKDF2
- [ ] Wallet PINs hashed
- [ ] Password validation enabled
- [ ] No plain text credentials in code

### 10. Final Checks
- [ ] Remove hardcoded credentials
- [ ] Verify `.gitignore` includes `.env`
- [ ] Test all authentication endpoints
- [ ] Verify CORS configuration
- [ ] Run security scan: `python manage.py check --deploy`
- [ ] Test backup restoration process

## Deployment Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run security check
python manage.py check --deploy

# Migrate database
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Start with Gunicorn
gunicorn Farmo.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## Post-Deployment
- [ ] Monitor logs for errors
- [ ] Test all critical endpoints
- [ ] Verify SSL certificate
- [ ] Check security headers
- [ ] Perform penetration testing
- [ ] Document incident response plan
