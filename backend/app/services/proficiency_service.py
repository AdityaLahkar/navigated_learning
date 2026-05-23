from app.extensions import db

from app.models.learning_activity import (
    LearningActivity
)

from app.models.learner_activity import (
    LearnerActivity
)

from app.models.learner_topic_progress import (
    LearnerTopicProgress
)


def calculate_topic_proficiency(
    learner_id,
    topic_id
):

    learning_activities = (
        LearningActivity.query.filter_by(
            topic_id=topic_id
        ).all()
    )

    if not learning_activities:
        return 0

    total_activities = len(
        learning_activities
    )

    total_score = 0

    for activity in learning_activities:

        learner_activity = (
            LearnerActivity.query.filter_by(
                learner_id=learner_id,
                activity_id=activity.id
            ).first()
        )

        if not learner_activity:
            continue

        normalized_score = (
            float(learner_activity.score) / 100
        )

        total_score += normalized_score

    proficiency_score = (
        total_score / total_activities
    )

    return round(
        proficiency_score,
        2
    )


def update_topic_proficiency(
    learner_id,
    topic_id
):

    proficiency_score = (
        calculate_topic_proficiency(
            learner_id,
            topic_id
        )
    )

    learner_progress = (
        LearnerTopicProgress.query.filter_by(
            learner_id=learner_id,
            topic_id=topic_id
        ).first()
    )

    if learner_progress:

        learner_progress.proficiency_score = (
            proficiency_score
        )

    else:

        learner_progress = (
            LearnerTopicProgress(
                learner_id=learner_id,
                topic_id=topic_id,
                proficiency_score=proficiency_score
            )
        )

        db.session.add(
            learner_progress
        )

    db.session.commit()

    return learner_progress