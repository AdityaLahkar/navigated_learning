from app.models.topic import Topic
from app.models.topic_prerequisite import TopicPrerequisite


def get_direct_prerequisites(topic_id):

    prerequisite_edges = TopicPrerequisite.query.filter_by(
        next_topic_id=topic_id
    ).all()

    prerequisite_topics = []

    for edge in prerequisite_edges:

        prerequisite_topics.append(
            edge.prerequisite_topic
        )

    return prerequisite_topics

def get_all_prerequisites(topic_id):

    visited = set()

    prerequisites = []

    def dfs(current_topic_id):

        prerequisite_edges = (
            TopicPrerequisite.query.filter_by(
                next_topic_id=current_topic_id
            ).all()
        )

        for edge in prerequisite_edges:

            prerequisite_topic = edge.prerequisite_topic

            if prerequisite_topic.id not in visited:

                visited.add(
                    prerequisite_topic.id
                )

                prerequisites.append(
                    prerequisite_topic
                )

                dfs(prerequisite_topic.id)

    dfs(topic_id)

    return prerequisites
