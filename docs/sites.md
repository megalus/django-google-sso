# Using Django Sites Framework

Django Google SSO supports the [Django Sites Framework](https://docs.djangoproject.com/en/stable/ref/contrib/sites/), allowing you to have different SSO configurations for different sites in your Django project.

## How It Works

Most configuration settings in Django Google SSO can now accept either a direct value or a callable function that receives the current request and returns the appropriate value for the current site.

This means you can dynamically determine configuration values based on the current site being accessed, enabling scenarios like:

- Different Google OAuth credentials per site
- Different user creation policies per site
- Different session timeouts per site

## Setup

1. First, ensure the Django Sites Framework is properly configured in your project:

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'django.contrib.sites',
    'django_google_sso',
    # ...
]

SITE_ID = 1  # Default site ID
```

2. Create your sites in the Django admin or via migrations.

3. Configure Django Google SSO settings as callables that return different values based on the current site:

```python
# settings.py
from django.contrib.sites.shortcuts import get_current_site

def get_client_id(request):
    """Return different client ID based on the current site."""
    site = get_current_site(request)

    # Map site domains to client IDs
    client_ids = {
        'example.com': 'client-id-for-example-com',
        'other-site.com': 'client-id-for-other-site',
    }

    return client_ids.get(site.domain, 'default-client-id')

# Configure settings as callables
GOOGLE_SSO_CLIENT_ID = get_client_id
```

## Example: Complete Site-Specific Configuration

Here's a more comprehensive example showing how to configure multiple settings per site:

```python
# settings.py
from django.contrib.sites.shortcuts import get_current_site

def get_site_config(request, config_key):
    """Get site-specific configuration."""
    site = get_current_site(request)

    # Define configurations for each site
    site_configs = {
        'example.com': {
            'client_id': 'client-id-for-example-com',
            'client_secret': 'secret-for-example-com',
            'project_id': 'project-id-for-example-com',
            'auto_create_users': True,
            'session_cookie_age': 3600,  # 1 hour
            'allowable_domains': ['example.com', 'example.org'],
        },
        'other-site.com': {
            'client_id': 'client-id-for-other-site',
            'client_secret': 'secret-for-other-site',
            'project_id': 'project-id-for-other-site',
            'auto_create_users': False,
            'session_cookie_age': 86400,  # 24 hours
            'allowable_domains': ['other-site.com'],
        }
    }

    # Get config for current site, or use defaults
    site_config = site_configs.get(site.domain, {})
    return site_config.get(config_key, None)

# Configure settings as callables
GOOGLE_SSO_CLIENT_ID = lambda request: get_site_config(request, 'client_id')
GOOGLE_SSO_CLIENT_SECRET = lambda request: get_site_config(request, 'client_secret')
GOOGLE_SSO_PROJECT_ID = lambda request: get_site_config(request, 'project_id')
GOOGLE_SSO_AUTO_CREATE_USERS = lambda request: get_site_config(request, 'auto_create_users')
GOOGLE_SSO_SESSION_COOKIE_AGE = lambda request: get_site_config(request, 'session_cookie_age')
GOOGLE_SSO_ALLOWABLE_DOMAINS = lambda request: get_site_config(request, 'allowable_domains')
```
!!! warning "Unsupported Settings for Callables"
    **All** settings support callable configuration, **except** the following:

    - `GOOGLE_SSO_ENABLED`
    - `GOOGLE_SSO_ENABLE_LOGS`
    - `SSO_USE_ALTERNATE_W003`
