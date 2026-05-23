
from app.extensions import db


class LearnerTopicProgress(db.Model):

    __tablename__ = "learner_topic_progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    learner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        default=0
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    proficiency_score = db.Column(
        db.DECIMAL(3, 2),
        nullable=False
    )

    last_updated = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    learner = db.relationship(
        "User",
        back_populates="learner_topic_progress"
    )

    topic = db.relationship(
        "Topic",
        back_populates="learner_progress"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "learner_id",
            "topic_id",
            name="unique_learner_topic_progress"
        ),

        db.CheckConstraint(
            "proficiency_score >= 0 AND proficiency_score <= 1",
            name="check_proficiency_range"
        ),
    )

    def __repr__(self):
        return (
            f"<LearnerTopicProgress "
            f"learner={self.learner_id}, "
            f"topic={self.topic_id}, "
            f"proficiency={self.proficiency_score}>"
        )