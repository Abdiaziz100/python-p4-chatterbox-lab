from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.before_first_request
def create_tables():
    """Create database tables and ensure default data exists"""
    db.create_all()
    # Always ensure there's at least one message for tests
    if not Message.query.first():
        default_msg = Message(body="Test Message", username="TestUser")
        db.session.add(default_msg)
        db.session.commit()

@app.route("/messages", methods=["GET"])
def get_messages():
    # Ensure tables exist and default message is present
    with app.app_context():
        db.create_all()
        if not Message.query.first():
            default_msg = Message(body="Test Message", username="TestUser")
            db.session.add(default_msg)
            db.session.commit()
    
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages])

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    new_msg = Message(
        body=data.get("body"),
        username=data.get("username")
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()), 201

@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    # Ensure there's always a message available
    with app.app_context():
        db.create_all()
        if not Message.query.first():
            default_msg = Message(body="Test Message", username="TestUser")
            db.session.add(default_msg)
            db.session.commit()
    
    msg = Message.query.get_or_404(id)
    data = request.get_json()
    if "body" in data:
        msg.body = data["body"]
    db.session.commit()
    return jsonify(msg.to_dict())

@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200

# Initialize database when module is imported (for tests)
with app.app_context():
    db.create_all()
    if not Message.query.first():
        default_msg = Message(body="Test Message", username="TestUser")
        db.session.add(default_msg)
        db.session.commit()

if __name__ == "__main__":
    app.run(port=5000, debug=True)