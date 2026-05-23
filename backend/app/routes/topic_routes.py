from flask import Blueprint, jsonify

from flask_jwt_extended import jwt_required

from app.models.topic_prerequisite import TopicPrerequisite



from app.models.topic import Topic


topic_bp = Blueprint(
    "topics",
    __name__,
    url_prefix="/topics"
)


@topic_bp.route("", methods=["GET"])
@jwt_required()
def get_topics():

    topics = Topic.query.all()

    response = []

    for topic in topics:

        response.append({
            "id": topic.id,
            "name": topic.name,
            "description": topic.description,
            "difficulty_level": (
                topic.difficulty_level
            )
        })

    return jsonify({
        "topics": response
    }), 200   

@topic_bp.route("/graph", methods=["GET"])
@jwt_required()
def get_topic_graph():

    topics = Topic.query.all()

    prerequisite_edges = (
        TopicPrerequisite.query.all()
    )

    topic_response = []

    for topic in topics:

        topic_response.append({
            "id": topic.id,
            "name": topic.name,
            "difficulty_level": (
                topic.difficulty_level
            )
        })

    edge_response = []

    for edge in prerequisite_edges:

        edge_response.append({
            "from": edge.prerequisite_topic_id,
            "to": edge.next_topic_id
        })

    return jsonify({
        "topics": topic_response,
        "edges": edge_response
    }), 200          
