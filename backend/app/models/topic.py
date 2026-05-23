
from app.extensions import db


class Topic(db.Model):

    __tablename__ = "topics"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    difficulty_level = db.Column(
        db.Enum("beginner", "intermediate", "advanced"),
        nullable=False
    )

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp()
    )

    learner_progress = db.relationship(
        "LearnerTopicProgress",
        back_populates="topic",
        cascade="all, delete-orphan"
    )

    learning_activities = db.relationship(
        "LearningActivity",
        back_populates="topic",
        cascade="all, delete-orphan"
    )

    prerequisite_edges = db.relationship(
        "TopicPrerequisite",
        foreign_keys="TopicPrerequisite.next_topic_id",
        back_populates="next_topic",
        cascade="all, delete-orphan"
    )

    dependent_edges = db.relationship(
        "TopicPrerequisite",
        foreign_keys="TopicPrerequisite.prerequisite_topic_id",
        back_populates="prerequisite_topic",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Topic {self.name}>"