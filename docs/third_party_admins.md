# Using Third Party Django Admins

Django has a great ecosystem, and many third-party apps are available to completely replace the default UI for Django Admin. We are trying to make Django Google SSO compatible as much as possible with these third-party apps. We can divide these apps broadly into two categories: apps which use the original Django Admin login template and apps with custom login templates.

??? question "How can I know if the third app has a custom login template?"
    Check if the app code contains the `templates/admin/login.html` file. If the file exists, the app has a custom login template.

## Apps with use original Django Admin login template
For these apps, Django Google SSO will work out of the box. You don't need to do anything special to make it work.

Some examples:

- [Django Admin Interface](https://github.com/fabiocaccamo/django-admin-interface)
- [Django Grappelli](https://github.com/sehmaschine/django-grappelli)
- [Django Jazzmin](https://github.com/farridav/django-jazzmin)
- [Django Jet Reboot](https://github.com/assem-ch/django-jet-reboot)

## Apps with custom login template
For these apps, you will need to create your own `admin/login.html` template to add both HTML from the custom login.html from the custom package and from this library, using this basic guideline:

### Create a custom `templates/admin/login.html` template
Suppose the `templates/admin/login.html` from the 3rd party app is using this structure:

```django
{% extends "third_app/base.html" %}

{% block my_form %}
    <form method="post" action="{% url 'admin:login' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Log in">
{% endblock %}
```

Please add on your project the `templates/admin/login.html` template:

```django
{% extends "admin/login.html" %}

{% block my_form %} {# Use the name of the block from the third-party app #}
    {{ block.super }} {# this will include the 3rd party app login.html content #}
    {% include "google_sso/login_sso.html" %} {# this will include the Google SSO login button #}
{% endblock %}
```

Now, let's add support to the `SSO_SHOW_FORM_ON_ADMIN_PAGE` option. To do this, update the code to include our `show_form` tag:

```django
{% extends "admin/login.html" %}
{% load show_form %}

{% block my_form %} {# Use the name of the block from the third-party app #}
    {% define_show_form as show_form %}
        {% if show_form %}
            {{ block.super }} {# this will include the 3rd party app login.html content #}
        {% endif %}
    {% include "google_sso/login_sso.html" %} {# this will include the Google SSO login button #}
{% endblock %}
```

!!! tip "This is a basic example."

    In real cases, you will need to understand how to find the correct elements to hide, and/or how to correct positioning the SSO buttons on the
    3rd party app layout. Use the real life example from `django-unfold` described below.

    Also, make sure you understand how Django works with [Template inheritance](https://docs.djangoproject.com/en/5.0/ref/templates/language/#template-inheritance)
    and [How to override templates](https://docs.djangoproject.com/en/5.0/howto/overriding-templates/).

### Current Custom Login Apps support

To this date, Django Google SSO provides support out of the box for these apps with custom login templates:

- [Django Unfold](https://github.com/unfoldadmin/django-unfold)

For the Django Unfold this is the code used on our login template:

```django
--8<-- "django_google_sso/templates/google_sso/login.html"
```

And this is the CSS you can use to customize your login button (you will need to create your custom `static/django_Microsoft_sso/microsoft_button.css/` to work):

```css
--8<-- "example_google_app/static/django_google_sso/google_button_unfold.css"
```
