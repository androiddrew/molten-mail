# Molten-mail Basic Example

## Installation
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
curl -X POST http://localhost:8000/?email=you@example.com
``` 