from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required
)

from sqlalchemy import func

from app.models.user import User

from app.models.topic import Topic

from app.models.learning_activity import (
    LearningActivity
)

from app.models.learner_activity import (
    LearnerActivity
)

from app.models.learner_topic_progress import (
    LearnerTopicProgress
)

from app.middleware.role_middleware import (
    role_required
)

from app.extensions import db

teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher"
)

@teacher_bp.route(
    "/dashboard",
    methods=["GET"]
)

@jwt_required()
@role_required("teacher")
def teacher_dashboard():

    # =====================================================
    # TOTAL LEARNERS
    # =====================================================

    total_learners = User.query.filter_by(
        role="learner"
    ).count()

    # =====================================================
    # AVERAGE PROFICIENCY
    # =====================================================

    average_proficiency = db.session.query(
        func.avg(
            LearnerTopicProgress.proficiency_score
        )
    ).scalar()

    if average_proficiency is None:
        average_proficiency = 0

    average_proficiency = round(
        float(average_proficiency),
        2
    )

    # =====================================================
    # MOST POPULAR TOPIC
    # =====================================================

    topic_activity_counts = db.session.query(
        LearningActivity.topic_id,
        func.count(
            LearnerActivity.id
        ).label("activity_count")
    ).join(
        LearnerActivity,
        LearningActivity.id ==
        LearnerActivity.activity_id
    ).group_by(
        LearningActivity.topic_id
    ).order_by(
        func.count(
            LearnerActivity.id
        ).desc()
    ).first()

    most_popular_topic = None

    if topic_activity_counts:

        topic = Topic.query.get(
            topic_activity_counts.topic_id
        )

        most_popular_topic = {
            "topic_id": topic.id,
            "topic_name": topic.name
        }

    # =====================================================
    # ACTIVITY DISTRIBUTION
    # =====================================================

    activity_distribution = {
        "reading": 0,
        "coding": 0,
        "quiz": 0,
        "discussion": 0
    }

    learner_activities = (
        LearnerActivity.query.all()
    )

    for learner_activity in learner_activities:

        activity_type = (
            learner_activity
            .learning_activity
            .activity_type
        )

        activity_distribution[
            activity_type
        ] += 1

    return jsonify({

        "total_learners": (
            total_learners
        ),

        "average_proficiency": (
            average_proficiency
        ),

        "most_popular_topic": (
            most_popular_topic
        ),

        "activity_distribution": (
            activity_distribution
        )

    }), 200


