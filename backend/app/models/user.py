
from app.extensions import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.Enum("learner", "teacher"),
        nullable=False
    )

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp()
    )

    learner_topic_progress = db.relationship(
        "LearnerTopicProgress",
        back_populates="learner",
        cascade="all, delete-orphan"
    )

    learner_activities = db.relationship(
        "LearnerActivity",
        back_populates="learner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"