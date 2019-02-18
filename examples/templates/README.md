# Molten-mail Template Example

This example demonstrates a more advanced handler, simulating the sending of a templated welcome email. This example includes the use of `threading.Thread` to send the email in an async fashion.

## Installation
*Note*: Template functionality requires [Jinja2](http://jinja.pocoo.org/docs/) to be installed. 

```
pip install -r requirements.txt
```

## Usage

Update the `MAIL` settings within `app.py` using the smtp settings of your provider.

Run your molten app:
```
gunicorn --reload app:app
```
Construct a POST request providing emails in the query string:
```
curl -X POST -H "Content-Type: application/json" --data '{"email": "you@example.com", "first_name": "Drew"}' http://localhost:8000/
``` 