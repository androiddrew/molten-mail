# molten-mail

[![PyPI](https://img.shields.io/pypi/v/molten-mail.svg)](https://pypi.org/project/molten-mail/)
[![PyPI](https://img.shields.io/pypi/pyversions/molten-mail.svg)](https://pypi.org/project/molten-mail/)
[![Build Status](https://travis-ci.org/androiddrew/molten-mail.svg?branch=master)](https://travis-ci.org/androiddrew/molten-mail)
[![codecov](https://codecov.io/gh/androiddrew/molten-mail/branch/master/graph/badge.svg)](https://codecov.io/gh/androiddrew/molten-mail)


Provides a simple interface to set up SMTP with your [Molten](https://github.com/Bogdanp/molten) web application and send messages from your handler functions. Please note this work derives largely from the [Flask-Mail](https://github.com/mattupstate/flask-mail) extension by 'Dan Jacob' and contributors, but has been modified extensively to remove Python 2 support and be used as a Molten component.


## Installation

`pip install molten-mail`

If you plan on using HTML templates you will need to ensure that [Jinja2] is installed. 

`pip install molten-mail[templates]`

## Usage

Be sure to check the [examples] folder for sample applications and more complex usage.

### Example Setup

To send mail messages from your view functions you must instantiate a `Mail` instance yourself or use the `MailComponent`. The `MailComponent` will instantiate a global `Mail` instance from settings provided in the `molten.Settings`.
 
Here we have a minimally viable app capable of sending an email message and returning a 204 response code:

```python
from molten import (
    App,
    Route,
    Settings,
    SettingsComponent,
    QueryParams,
    HTTP_204,
    HTTP_400,
    Response,
)
from molten_mail import MailComponent, Mail, Message

# Replace with your own SMTP parameters
settings = Settings(
    {
        "MAIL_SERVER": "smtp.example.com",
        "MAIL_USERNAME": "me@example.com",
        "MAIL_PASSWORD": "dontaddthistoyourversioncontrol",
        "MAIL_PORT": 587,
        "MAIL_USE_TLS": True,
        "MAIL_DEFAULT_SENDER": "me@example.com",
    }
)


def send_message(params: QueryParams, mail: Mail):
    """Emails an email address provided in the query string"""
    addresses = params.get_all("email")
    if not addresses:
        return Response(
            HTTP_400,
            content="Provide emails in the query params to send a welcome message",
        )
    msg = Message(
        subject="Welcome to Molten!",
        body="Welcome to Molten! Glad to have you here.",
        recipients=addresses,
    )
    mail.send(msg)
    return Response(HTTP_204, content="")


routes = [Route("/", send_message, "POST")]

components = [SettingsComponent(settings), MailComponent()]

app = App(routes=routes, components=components)
```

### Configuration Options

A singleton `Mail` component can be configured for use in dependency injection using options included in your `molten.Settings`. This requires that you include the `MailComponent` within you `molten.App` instance. The key values can either be all upper or lowercase and begin with `MAIL_`. The available options are:

* 'MAIL_SERVER': default 'localhost'
* 'MAIL_USERNAME': default None
* 'MAIL_PASSWORD': default None
* 'MAIL_PORT': default 25
* 'MAIL_USE_TLS': default False
* 'MAIL_USE_SSL': default False
* 'MAIL_DEFAULT_SENDER': default None
* 'MAIL_DEBUG': default False
* 'MAIL_MAX_EMAILS': default None
* 'MAIL_SUPPRESS_SEND': default False
* 'MAIL_ASCII_ATTACHMENTS': False



### Sending Messages

To send a message, instantiate a `Mail` component. Then create an instance of `Message`, and pass it to your `Mail` component using `mail.send(msg)`

```python
from molten_mail import Mail, Message

mail = Mail(server="localhost",
            user="me@example.com",
            password="dontaddthistoyourversioncontrol",
            port=587,
            use_tls=True,
            default_sender="me@example.com")
msg = Message(subject="Hey there!", body="Welcome to Molten Mail", recipients=["you@example.com"])
mail.send(msg)

```

Your message recipients can be set in bulk or individually:

```python
msg.recipients = ['you@example.com', 'me@example.com']
msg.add_recipient('otherperson@example.com')
```

If you have included a default sender you do not need to set the message sender explicitly, as it will use this configuration value by default:

```python
msg = Message('Hello',
              recipients=['you@example.com'])
```

The sender can also be passed as a two element tuple containing a name and email address which will be split like so:

```python
msg = Message('Hello',
              sender=('Me', 'me@example.com'))

assert msg.sender == 'Me <me@example.com>'
```

A Message can contain a body and/or HTML:

```python
msg.body = 'message body'
msg.html = '<b>Hello Molten-mail!</b>'
```

A convenience function `send_message` can also be used to create and send a message:

```python
mail.send_message(subject="Your subject", body="Message body", recipients=["you@example.com"])
```

### HTML Email Templates

Molten-mail includes a convenience component `MailTemplates` for rendering HTML email bodies using [Jinja2]. You have to install `jinja2` yourself before using this module.
 
You must include the `MailTemplatesComponent` in your app, passing the path to a folder containing your templates. 

```python
from molten import App, Route, Response, HTTP_204, Settings, SettingsComponent
from molten_mail import Mail, MailComponent
from molten_mail.templates import MailTemplates, MailTemplatesComponent

settings = Settings({
    ...
})

def view_func(mail: Mail, mail_templates: MailTemplates): -> Response:
    mail.send_message(
        subject="Hello Molten!",
        html=mail_templates.render("my_email_template.html", somevalue="Key values for the template context"),
        recipients=["you@example.com"]
    )
    return Response(HTTP_204, content="")

app = App(
    components=[SettingsComponent(settings),
                MailComponent(),
                MailTemplatesComponent('./path_to_templates_dir')],
    routes=[Route('/', view_func, method="POST"]
)

```


## Testing

To run the test suite with coverage first install the package in editable mode with it's full testing requirements:

`$ pip install -e ".[dev]"`

To run the project's tests

`$ pytest --cov`

To run tests against multiple python interpreters use:

`$ tox`

[Jinja2]: http://jinja.pocoo.org/docs/
[examples]: https://github.com/androiddrew/molten-mail/tree/master/examples