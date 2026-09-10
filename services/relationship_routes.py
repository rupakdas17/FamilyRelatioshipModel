from flask import Blueprint, request, jsonify

from models.member_model import (
    members_collection,
    relationships_collection
)

from services.relationship_service import (
    find_relationship_path
)


relationship_routes = Blueprint(
    "relationship_routes",
    __name__
)


# -----------------------------
# ADD RELATIONSHIP
# -----------------------------

@relationship_routes.route(
    "/relationships",
    methods=["POST"]
)
def add_relationship():

    data = request.json

    person1_id = data.get("person1_id")
    person2_id = data.get("person2_id")
    relationship = data.get("relationship")

    if not person1_id or not person2_id:

        return jsonify({
            "error": "Both persons are required"
        }), 400

    if not relationship:

        return jsonify({
            "error": "Relationship is required"
        }), 400

    if person1_id == person2_id:

        return jsonify({
            "error": "A person cannot be related to themselves"
        }), 400

    relationship_data = {

        "person1_id": person1_id,

        "person2_id": person2_id,

        "relationship": relationship
    }

    relationships_collection.insert_one(
        relationship_data
    )

    return jsonify({
        "message": "Relationship added successfully"
    }), 201


# -----------------------------
# GET RELATIONSHIPS
# -----------------------------

@relationship_routes.route(
    "/relationships",
    methods=["GET"]
)
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
# FIND RELATIONSHIP
# -----------------------------

@relationship_routes.route(
    "/relationship/<person1_id>/<person2_id>",
    methods=["GET"]
)
def find_relationship(person1_id, person2_id):

    members = list(
        members_collection.find()
    )

    relationships = list(
        relationships_collection.find()
    )

    path = find_relationship_path(
        members,
        relationships,
        person1_id,
        person2_id
    )

    if path is None:

        return jsonify({
            "message": "No relationship found"
        }), 404

    return jsonify({

        "relationship_path": path,

        "relationship": " → ".join(path)

    })