# Auto Create Users

**Django Google SSO** can automatically create users from Google SSO authentication. To enable this feature, you need to
set the `GOOGLE_SSO_ALLOWABLE_DOMAINS` setting in your `settings.py`, with a list of domains that will be allowed to create.
For example, if any user with a gmail account can sign in, you can set:

```python
# settings.py

GOOGLE_SSO_ALLOWABLE_DOMAINS = ["gmail.com"]
```

## Disabling the auto-create users

You can disable the auto-create users feature by setting the `GOOGLE_SSO_AUTO_CREATE_USERS` setting to `False`:

```python
GOOGLE_SSO_AUTO_CREATE_USERS = False
```

You can also disable the plugin completely:

```python

GOOGLE_SSO_ENABLED = False
```

## Giving Permissions to Auto-Created Users

If you are using the auto-create users feature, you can give permissions to the users that are created automatically. To do
this you can set the following options in your `settings.py`:

```python
# List of emails that will be created as staff
GOOGLE_SSO_STAFF_LIST = ["my-email@my-domain.com"]

# List of emails that will be created as superuser
GOOGLE_SSO_SUPERUSER_LIST = ["another-email@my-domain.com"]

# If True, the first user that logs in will be created as superuser
# if no superuser exists in the database at all
GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER = True
```

!!! warning "Be careful with these options"
    The idea here is to make your life easier, especially when testing. But if you are not careful, you can give
    permissions to users that you don't want, or even worse, you can give permissions to users that you don't know.
    So, please, be careful with these options.

---

For the last step, we will look at the Django URLs.
