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
