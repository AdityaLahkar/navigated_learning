from app import create_app

from app.extensions import db

from app.models.user import User

from app.models.topic import Topic

from app.models.topic_prerequisite import (
    TopicPrerequisite
)

from app.models.learning_activity import (
    LearningActivity
)

from app.models.learner_activity import (
    LearnerActivity
)

from app.models.learner_topic_progress import (
    LearnerTopicProgress
)

from app.services.proficiency_service import (
    calculate_topic_proficiency
)

from app.utils.auth_utils import (
    hash_password
)


app = create_app()


with app.app_context():

    existing_topic = Topic.query.filter_by(
        name="Programming Basics"
    ).first()

    if existing_topic:
        print("Seed data already exists")
        exit()

    # =========================================================
    # USERS
    # =========================================================

    users = [

        User(
            name="Beginner Learner",
            email="beginner@test.com",
            password_hash=hash_password(
                "password123"
            ),
            role="learner"
        ),

        User(
            name="Intermediate Learner",
            email="intermediate@test.com",
            password_hash=hash_password(
                "password123"
            ),
            role="learner"
        ),

        User(
            name="Advanced Learner",
            email="advanced@test.com",
            password_hash=hash_password(
                "password123"
            ),
            role="learner"
        ),

        User(
            name="Teacher User",
            email="teacher@test.com",
            password_hash=hash_password(
                "password123"
            ),
            role="teacher"
        )
    ]

    db.session.add_all(users)

    db.session.commit()

    # =========================================================
    # TOPICS
    # =========================================================

    topics = [

        Topic(
            name="Programming Basics",
            description="Introduction to programming",
            difficulty_level="beginner"
        ),

        Topic(
            name="Data Structures",
            description="Core data structures",
            difficulty_level="beginner"
        ),

        Topic(
            name="Algorithms",
            description="Algorithmic problem solving",
            difficulty_level="intermediate"
        ),

        Topic(
            name="Dynamic Programming",
            description="Optimization techniques",
            difficulty_level="advanced"
        ),

        Topic(
            name="Discrete Mathematics",
            description="Mathematical foundations",
            difficulty_level="beginner"
        ),

        Topic(
            name="Probability",
            description="Probability fundamentals",
            difficulty_level="intermediate"
        ),

        Topic(
            name="Linear Algebra",
            description="Matrices and vectors",
            difficulty_level="intermediate"
        ),

        Topic(
            name="Machine Learning",
            description="ML fundamentals",
            difficulty_level="advanced"
        )
    ]

    db.session.add_all(topics)

    db.session.commit()

    topic_map = {
        topic.name: topic
        for topic in Topic.query.all()
    }

    # =========================================================
    # TOPIC PREREQUISITES
    # =========================================================

    prerequisites = [

        TopicPrerequisite(
            prerequisite_topic_id=topic_map[
                "Programming Basics"
            ].id,

            next_topic_id=topic_map[
                "Data Structures"
            ].id
        ),

        TopicPrerequisite(
            prerequisite_topic_id=topic_map[
                "Data Structures"
            ].id,

            next_topic_id=topic_map[
                "Algorithms"
            ].id
        ),

        TopicPrerequisite(
            prerequisite_topic_id=topic_map[
                "Algorithms"
            ].id,

            next_topic_id=topic_map[
                "Dynamic Programming"
            ].id
        ),

        TopicPrerequisite(
            prerequisite_topic_id=topic_map[
                "Discrete Mathematics"
            ].id,

            next_topic_id=topic_map[
                "Probability"
            ].id
        ),

        TopicPrerequisite(
            prerequisite_topic_id=topic_map[
                "Probability"
            ].id,

            next_topic_id=topic_map[
                "Machine Learning"
            ].id
        ),

        TopicPrerequisite(
            prerequisite_topic_id=topic_map[
                "Linear Algebra"
            ].id,

            next_topic_id=topic_map[
                "Machine Learning"
            ].id
        )
    ]

    db.session.add_all(prerequisites)

    db.session.commit()

    # =========================================================
    # LEARNING ACTIVITIES
    # =========================================================

    activities = [

        # Programming Basics

        LearningActivity(
            topic_id=topic_map[
                "Programming Basics"
            ].id,
            activity_type="reading",
            activity_name="Programming Basics Notes"
        ),

        LearningActivity(
            topic_id=topic_map[
                "Programming Basics"
            ].id,
            activity_type="quiz",
            activity_name="Programming Basics Quiz"
        ),

        # Data Structures

        LearningActivity(
            topic_id=topic_map[
                "Data Structures"
            ].id,
            activity_type="coding",
            activity_name="Linked List Implementation"
        ),

        LearningActivity(
            topic_id=topic_map[
                "Data Structures"
            ].id,
            activity_type="quiz",
            activity_name="Stacks and Queues Quiz"
        ),

        # Algorithms

        LearningActivity(
            topic_id=topic_map[
                "Algorithms"
            ].id,
            activity_type="quiz",
            activity_name="Sorting Algorithms Quiz"
        ),

        LearningActivity(
            topic_id=topic_map[
                "Algorithms"
            ].id,
            activity_type="coding",
            activity_name="Binary Search Implementation"
        ),

        # Dynamic Programming

        LearningActivity(
            topic_id=topic_map[
                "Dynamic Programming"
            ].id,
            activity_type="coding",
            activity_name="Knapsack Problem"
        ),

        # Discrete Mathematics

        LearningActivity(
            topic_id=topic_map[
                "Discrete Mathematics"
            ].id,
            activity_type="reading",
            activity_name="Discrete Mathematics Notes"
        ),

        # Probability

        LearningActivity(
            topic_id=topic_map[
                "Probability"
            ].id,
            activity_type="quiz",
            activity_name="Bayes Quiz 1"
        ),

        LearningActivity(
            topic_id=topic_map[
                "Probability"
            ].id,
            activity_type="quiz",
            activity_name="Bayes Quiz 2"
        ),

        # Linear Algebra

        LearningActivity(
            topic_id=topic_map[
                "Linear Algebra"
            ].id,
            activity_type="coding",
            activity_name="Matrix Operations"
        ),

        # Machine Learning

        LearningActivity(
            topic_id=topic_map[
                "Machine Learning"
            ].id,
            activity_type="coding",
            activity_name="Linear Regression Project"
        )
    ]

    db.session.add_all(activities)

    db.session.commit()

    activity_map = {
        activity.activity_name: activity
        for activity in LearningActivity.query.all()
    }

    learner_map = {
        learner.email: learner
        for learner in User.query.filter_by(
            role="learner"
        ).all()
    }

    # =========================================================
    # LEARNER ACTIVITIES
    # =========================================================

    learner_activities = [

        # =====================================================
        # BEGINNER LEARNER
        # =====================================================

        LearnerActivity(
            learner_id=learner_map[
                "beginner@test.com"
            ].id,

            activity_id=activity_map[
                "Programming Basics Notes"
            ].id,

            score=90,

            duration_minutes=40
        ),

        LearnerActivity(
            learner_id=learner_map[
                "beginner@test.com"
            ].id,

            activity_id=activity_map[
                "Programming Basics Quiz"
            ].id,

            score=82,

            duration_minutes=20
        ),

        # =====================================================
        # INTERMEDIATE LEARNER
        # =====================================================

        LearnerActivity(
            learner_id=learner_map[
                "intermediate@test.com"
            ].id,

            activity_id=activity_map[
                "Programming Basics Notes"
            ].id,

            score=95,

            duration_minutes=35
        ),

        LearnerActivity(
            learner_id=learner_map[
                "intermediate@test.com"
            ].id,

            activity_id=activity_map[
                "Programming Basics Quiz"
            ].id,

            score=92,

            duration_minutes=18
        ),

        LearnerActivity(
            learner_id=learner_map[
                "intermediate@test.com"
            ].id,

            activity_id=activity_map[
                "Linked List Implementation"
            ].id,

            score=80,

            duration_minutes=60
        ),

        LearnerActivity(
            learner_id=learner_map[
                "intermediate@test.com"
            ].id,

            activity_id=activity_map[
                "Stacks and Queues Quiz"
            ].id,

            score=75,

            duration_minutes=25
        ),

        LearnerActivity(
            learner_id=learner_map[
                "intermediate@test.com"
            ].id,

            activity_id=activity_map[
                "Sorting Algorithms Quiz"
            ].id,

            score=50,

            duration_minutes=30
        ),

        # =====================================================
        # ADVANCED LEARNER
        # =====================================================

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Programming Basics Notes"
            ].id,

            score=100,

            duration_minutes=20
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Programming Basics Quiz"
            ].id,

            score=98,

            duration_minutes=10
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Linked List Implementation"
            ].id,

            score=95,

            duration_minutes=40
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Stacks and Queues Quiz"
            ].id,

            score=92,

            duration_minutes=20
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Sorting Algorithms Quiz"
            ].id,

            score=90,

            duration_minutes=20
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Binary Search Implementation"
            ].id,

            score=88,

            duration_minutes=40
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Discrete Mathematics Notes"
            ].id,

            score=93,

            duration_minutes=50
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Bayes Quiz 1"
            ].id,

            score=84,

            duration_minutes=25
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Bayes Quiz 2"
            ].id,

            score=86,

            duration_minutes=22
        ),

        LearnerActivity(
            learner_id=learner_map[
                "advanced@test.com"
            ].id,

            activity_id=activity_map[
                "Matrix Operations"
            ].id,

            score=81,

            duration_minutes=45
        )
    ]

    db.session.add_all(
        learner_activities
    )

    db.session.commit()

    # =========================================================
    # LEARNER TOPIC PROGRESS
    # =========================================================

    learner_progress_entries = []

    learners = User.query.filter_by(
        role="learner"
    ).all()

    topics = Topic.query.all()

    for learner in learners:

        for topic in topics:

            proficiency_score = (
                calculate_topic_proficiency(
                    learner.id,
                    topic.id
                )
            )

            if proficiency_score > 0:

                learner_progress_entries.append(

                    LearnerTopicProgress(
                        learner_id=learner.id,
                        topic_id=topic.id,
                        proficiency_score=proficiency_score
                    )
                )

    db.session.add_all(
        learner_progress_entries
    )

    db.session.commit()

    print("Seed data inserted successfully")