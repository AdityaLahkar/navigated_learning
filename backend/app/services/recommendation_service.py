from app.models.topic import Topic

from app.models.learner_topic_progress import (
    LearnerTopicProgress
)

from app.services.graph_service import (
    get_direct_prerequisites
)

MASTERY_THRESHOLD = 0.7

def is_topic_mastered(
    learner_id,
    topic_id
):

    learner_progress = (
        LearnerTopicProgress.query.filter_by(
            learner_id=learner_id,
            topic_id=topic_id
        ).first()
    )

    if not learner_progress:
        return False

    return (
        learner_progress.proficiency_score
        >= MASTERY_THRESHOLD
    )

def get_recommended_topics(
    learner_id
):

    recommended_topics = []

    all_topics = Topic.query.all()

    for topic in all_topics:

        if is_topic_mastered(
            learner_id,
            topic.id
        ):
            continue

        prerequisites = (
            get_direct_prerequisites(
                topic.id
            )
        )

        prerequisites_satisfied = True

        for prerequisite in prerequisites:

            if not is_topic_mastered(
                learner_id,
                prerequisite.id
            ):

                prerequisites_satisfied = False
                break

        if prerequisites_satisfied:

            recommended_topics.append(
                topic
            )

    return recommended_topics
