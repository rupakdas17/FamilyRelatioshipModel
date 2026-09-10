from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId

from models.member_model import members_collection
from models.member_model import relationships_collection


member_routes = Blueprint(
    "member_routes",
    __name__
)


# -----------------------------
# ADD MEMBER
# -----------------------------

@member_routes.route("/members", methods=["POST"])
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

@member_routes.route("/members", methods=["GET"])
def get_members():

    members = []

    for member in members_collection.find():

        members.append({
            "id": str(member["_id"]),
            "name": member.get("name"),
            "age": member.get("age"),
            "gender": member.get("gender")
        })

    return jsonify(members)


# -----------------------------
# DELETE MEMBER
# -----------------------------

@member_routes.route("/members/<member_id>", methods=["DELETE"])
def delete_member(member_id):

    try:

        result = members_collection.delete_one({
            "_id": ObjectId(member_id)
        })

        if result.deleted_count == 0:

            return jsonify({
                "error": "Member not found"
            }), 404

        # Delete connected relationships
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