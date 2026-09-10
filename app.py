from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["family_relationship_db"]

# Collections
members_collection = db["members"]
relationships_collection = db["relationships"]


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Family Relationship Model API is running"
    })


# -----------------------------
# ADD MEMBER
# -----------------------------
@app.route("/members", methods=["POST"])
def add_member():

    data = request.json

    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")

    if not name:
        return jsonify({
            "error": "Name is required"
        }), 400

    member = {
        "name": name,
        "age": age,
        "gender": gender
    }

    result = members_collection.insert_one(member)

    return jsonify({
        "message": "Member added successfully",
        "id": str(result.inserted_id)
    }), 201


# -----------------------------
# GET ALL MEMBERS
# -----------------------------
@app.route("/members", methods=["GET"])
def get_members():

    members = []

    for member in members_collection.find():

        members.append({
            "id": str(member["_id"]),
            "name": member["name"],
            "age": member.get("age"),
            "gender": member.get("gender")
        })

    return jsonify(members)


# -----------------------------
# DELETE MEMBER
# -----------------------------
@app.route("/members/<member_id>", methods=["DELETE"])
def delete_member(member_id):

    try:
        result = members_collection.delete_one({
            "_id": ObjectId(member_id)
        })

        if result.deleted_count == 0:
            return jsonify({
                "error": "Member not found"
            }), 404

        # Delete relationships connected to this member
        relationships_collection.delete_many({
            "$or": [
                {"person1_id": member_id},
                {"person2_id": member_id}
            ]
        })

        return jsonify({
            "message": "Member deleted successfully"
        })

    except Exception:
        return jsonify({
            "error": "Invalid member ID"
        }), 400


# -----------------------------
# ADD RELATIONSHIP
# -----------------------------
@app.route("/relationships", methods=["POST"])
def add_relationship():

    data = request.json

    person1_id = data.get("person1_id")
    person2_id = data.get("person2_id")
    relationship = data.get("relationship")

    if not person1_id or not person2_id or not relationship:
        return jsonify({
            "error": "All fields are required"
        }), 400

    relationship_data = {
        "person1_id": person1_id,
        "person2_id": person2_id,
        "relationship": relationship
    }

    relationships_collection.insert_one(relationship_data)

    return jsonify({
        "message": "Relationship added successfully"
    }), 201


# -----------------------------
# GET ALL RELATIONSHIPS
# -----------------------------
@app.route("/relationships", methods=["GET"])
def get_relationships():

    relationships = []

    for relation in relationships_collection.find():

        relationships.append({
            "id": str(relation["_id"]),
            "person1_id": relation["person1_id"],
            "person2_id": relation["person2_id"],
            "relationship": relation["relationship"]
        })

    return jsonify(relationships)


# -----------------------------
# FIND DIRECT RELATIONSHIP
# -----------------------------
@app.route("/relationship/<person1_id>/<person2_id>", methods=["GET"])
def find_relationship(person1_id, person2_id):

    relation = relationships_collection.find_one({
        "person1_id": person1_id,
        "person2_id": person2_id
    })

    if relation:

        return jsonify({
            "relationship": relation["relationship"]
        })

    # Check reverse relationship
    relation = relationships_collection.find_one({
        "person1_id": person2_id,
        "person2_id": person1_id
    })

    if relation:

        return jsonify({
            "relationship": relation["relationship"]
        })

    return jsonify({
        "message": "No direct relationship found"
    }), 404


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)