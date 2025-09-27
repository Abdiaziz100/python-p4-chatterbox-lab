from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

# Create Flask app
app = Flask(__name__)
CORS(app)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# -----------------------
# ROUTES
# -----------------------

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data.get("body"),
        username=data.get("username")
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if "body" in data:
        message.body = data["body"]
    db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)