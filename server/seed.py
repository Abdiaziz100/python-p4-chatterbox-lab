from app import app, db
from models import Message

# Seed data
messages = [
    {"body": "Hello, World!", "username": "Abdiaziz"},
    {"body": "This is Flask + React 🚀", "username": "Mahat"},
    {"body": "Full-stack development is fun!", "username": "ChatGPT"},
]

with app.app_context():
    print("Seeding database...")

    # Delete old records
    Message.query.delete()

    # Add new messages
    for msg in messages:
        message = Message(body=msg["body"], username=msg["username"])
        db.session.add(message)

    db.session.commit()
    print("Done seeding ✅")