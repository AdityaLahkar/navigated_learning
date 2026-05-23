
from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.models.user import User

from app.services.recommendation_service import (
    get_recommended_topics
)

from app.models.topic_prerequisite import (
    TopicPrerequisite
)

from app.models.learner_topic_progress import (
    LearnerTopicProgress
)

from app.models.learner_activity import (
    LearnerActivity
)

from app.models.learning_activity import (
    LearningActivity
)

import math

learner_bp = Blueprint(
    "learners",
    __name__,
    url_prefix="/learners"
)

@learner_bp.route(
    "/<int:learner_id>/recommendations",
    methods=["GET"]
)

@jwt_required()
def learner_recommendations(
    learner_id
):

    current_user_id = int(
        get_jwt_identity()
    )

    current_user_role = (
        get_jwt()["role"]
    )

    learner = User.query.filter_by(
        id=learner_id,
        role="learner"
    ).first()

    if not learner:

        return jsonify({
            "error": "Learner not found"
        }), 404

    # =====================================================
    # RBAC CHECK
    # =====================================================

    if (
        current_user_role == "learner"
        and
        current_user_id != learner_id
    ):

        return jsonify({
            "error": "Forbidden"
        }), 403

    recommended_topics = (
        get_recommended_topics(
            learner_id
        )
    )

    response = []

    for topic in recommended_topics:

        response.append({
            "topic_id": topic.id,
            "topic_name": topic.name,
            "reason": (
                "All prerequisites exceed "
                "70% proficiency"
            )
        })

    return jsonify({
        "learner_id": learner_id,
        "recommendations": response
    }), 200


@learner_bp.route(
    "/<int:learner_id>/map",
    methods=["GET"]
)

@jwt_required()
def learner_map(
    learner_id
):

    current_user_id = int(
        get_jwt_identity()
    )

    current_user_role = (
        get_jwt()["role"]
    )

    learner = User.query.filter_by(
        id=learner_id,
        role="learner"
    ).first()

    if not learner:

        return jsonify({
            "error": "Learner not found"
        }), 404

    # =====================================================
    # RBAC CHECK
    # =====================================================

    if (
        current_user_role == "learner"
        and
        current_user_id != learner_id
    ):

        return jsonify({
            "error": "Forbidden"
        }), 403

    learner_progress = (
        LearnerTopicProgress.query.filter_by(
            learner_id=learner_id
        ).all()
    )

    topics_response = []

    topic_ids = set()

    for progress in learner_progress:

        topics_response.append({
            "id": progress.topic.id,
            "name": progress.topic.name,
            "proficiency": float(
                progress.proficiency_score
            )
        })

        topic_ids.add(
            progress.topic.id
        )

    prerequisite_edges = (
        TopicPrerequisite.query.all()
    )

    edges_response = []

    for edge in prerequisite_edges:

        if (
            edge.prerequisite_topic_id
            in topic_ids
            and
            edge.next_topic_id
            in topic_ids
        ):

            edges_response.append({
                "from": edge.prerequisite_topic_id,
                "to": edge.next_topic_id
            })

    return jsonify({
        "learner_id": learner_id,
        "topics": topics_response,
        "edges": edges_response
    }), 200

@learner_bp.route(
    "/<int:learner_id>/activities",
    methods=["GET"]
)

@jwt_required()
def learner_activities(
    learner_id
):

    current_user_id = int(
        get_jwt_identity()
    )

    current_user_role = (
        get_jwt()["role"]
    )

    learner = User.query.filter_by(
        id=learner_id,
        role="learner"
    ).first()

    if not learner:

        return jsonify({
            "error": "Learner not found"
        }), 404

    # =====================================================
    # RBAC CHECK
    # =====================================================

    if (
        current_user_role == "learner"
        and
        current_user_id != learner_id
    ):

        return jsonify({
            "error": "Forbidden"
        }), 403

    learner_activity_rows = (
        LearnerActivity.query.filter_by(
            learner_id=learner_id
        ).all()
    )

    activity_counts = {
        "reading": 0,
        "coding": 0,
        "quiz": 0,
        "discussion": 0
    }

    for learner_activity in learner_activity_rows:

        activity_type = (
            learner_activity
            .learning_activity
            .activity_type
        )

        activity_counts[
            activity_type
        ] += 1

    # =====================================================
    # DOMINANT ACTIVITY
    # =====================================================

    dominant_activity = max(
        activity_counts,
        key=activity_counts.get
    )

    # =====================================================
    # DIVERSITY SCORE
    # =====================================================

    total_activities = sum(
        activity_counts.values()
    )

    entropy = 0

    for count in activity_counts.values():

        if count > 0:

            probability = (
                count / total_activities
            )

            entropy -= (
                probability *
                math.log2(probability)
            )

    max_entropy = math.log2(4)

    activity_diversity_score = round(
        entropy / max_entropy,
        2
    )

    return jsonify({
        "learner_id": learner_id,

        "activities": activity_counts,

        "activity_diversity_score": (
            activity_diversity_score
        ),

        "dominant_activity": (
            dominant_activity
        )
    }), 200