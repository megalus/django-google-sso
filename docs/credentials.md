# Adding Google Credentials

To make the SSO work, we need to set up, in your Django project, the Google credentials needed to perform the
authentication.

---

## Getting Google Credentials

In your [Google Console](https://console.cloud.google.com/apis/credentials) navigate to _Api -> Credentials_ to access
the credentials for your all Google Cloud Projects.

!!! tip "Your first Google Cloud Project"
    If you don't have a Google Cloud Project, you can create one by clicking on the _**Create**_ button.

Then, you can select one of existing Web App Oauth 2.0 Client Ids in your Google project, or create a new one.

??? question "Do I need to create a new Oauth 2.0 Client Web App?"
    Normally you will have one credential per environment in your Django project. For example, if you have
    a _development_, _staging_ and _production_ environments, then you will have three credentials, one for each one.
    This mitigates the risk of exposing all your data in case of a security breach.

    If you decide to create a new one, please check https://developers.google.com/identity/protocols/oauth2/ for additional info.

When you open your Web App Client Id, please get the following information:

* The **Client ID**. This is something like `XXXX.apps.googleusercontent.com` and will be the `GOOGLE_SSO_CLIENT_ID` in
  your Django project.
* The **Client Secret Key**. This is a long string and will be the `GOOGLE_SSO_CLIENT_SECRET` in your Django project.
* The **Project ID**. This is the Project ID, you can get click on the Project Name, and will be
  the `GOOGLE_SSO_PROJECT_ID` in your Django project.

After that, add them in your `settings.py` file:

```python
# settings.py
GOOGLE_SSO_CLIENT_ID = "your client id here"
GOOGLE_SSO_CLIENT_SECRET = "your client secret here"
GOOGLE_SSO_PROJECT_ID = "your project id here"
```

Don't commit this info in your repository.
This permits you to have different credentials for each environment and mitigates security breaches.
That's why we recommend you to use environment variables to store this info.
To read this data, we recommend you to install and use a [Twelve-factor compatible](https://www.12factor.net/) library
in your project.

For example, you can use our [sister project Stela](https://github.com/megalus/stela) to load the environment
variables from a `.env.local` file, like this:

```ini
# .env.local
GOOGLE_SSO_CLIENT_ID="your client id here"
GOOGLE_SSO_CLIENT_SECRET="your client secret here"
GOOGLE_SSO_PROJECT_ID="your project id here"
```

```python
# Django settings.py
from stela import env

GOOGLE_SSO_CLIENT_ID = env.GOOGLE_SSO_CLIENT_ID
GOOGLE_SSO_CLIENT_SECRET = env.GOOGLE_SSO_CLIENT_SECRET
GOOGLE_SSO_PROJECT_ID = env.GOOGLE_SSO_PROJECT_ID
```

But in fact, you can use any library you want, like
[django-environ](https://pypi.org/project/django-environ/), [django-constance](https://github.com/jazzband/django-constance),
[python-dotenv](https://pypi.org/project/python-dotenv/), etc...

---

In the next step, we need to configure the authorized callback URI for your Django project.
