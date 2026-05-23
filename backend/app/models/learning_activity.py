
from app.extensions import db


class LearningActivity(db.Model):

    __tablename__ = "learning_activities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    activity_type = db.Column(
        db.Enum(
            "reading",
            "coding",
            "quiz",
            "discussion"
        ),
        nullable=False
    )

    activity_name = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp()
    )

    topic = db.relationship(
        "Topic",
        back_populates="learning_activities"
    )

    learner_activities = db.relationship(
        "LearnerActivity",
        back_populates="learning_activity",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<LearningActivity "
            f"{self.activity_name}>"
        )