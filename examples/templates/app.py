from threading import Thread
from molten import App, Route, Settings, SettingsComponent, schema, HTTP_204, Response
from molten_mail import MailComponent, Mail, Message
from molten_mail.templates import MailTemplates, MailTemplatesComponent

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


@schema
class Signup:
    email: str
    first_name: str


def send_async_email(mail: Mail, msg: Message) -> None:
    mail.send(msg)


def sign_up(signup: Signup, mail: Mail, templates: MailTemplates):
    """Handler that simulates a basic async sending of an html templated welcome email"""
    msg = Message(
        subject="Welcome to Molten!",
        body="This is a body that gets shown if html can't",
        html=templates.render("welcome_mail.html", name=signup.first_name),
        recipients=[signup.email],
    )
    Thread(target=send_async_email, args=(mail, msg)).start()
    return Response(HTTP_204, content="")


routes = [Route("/", sign_up, "POST")]

components = [
    SettingsComponent(settings),
    MailComponent(),
    MailTemplatesComponent("templates"),
]

app = App(routes=routes, components=components)
