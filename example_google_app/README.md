## Django Example App

## Start the Project

Please create a `.env` file with the following information:

```dotenv
GOOGLE_SSO_ALLOWABLE_DOMAINS=gmail.com
GOOGLE_SSO_CLIENT_ID=<your web app client id>
GOOGLE_SSO_CLIENT_SECRET=<your web app client secret>
GOOGLE_SSO_PROJECT_ID=<your google project id>
GOOGLE_SSO_CALLBACK_DOMAIN=localhost:8000
```

Then run the following commands:

```shell
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Open browser in `http://localhost:8000/secret`

## Django Admin skins

Please uncomment on `settings.py` the correct app for the skin you want to test, in `INSTALLED_APPS`.
