from app.extensions import db


class LearnerActivity(db.Model):

    __tablename__ = "learner_activities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    learner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("learning_activities.id"),
        nullable=False
    )

    score = db.Column(
        db.DECIMAL(5, 2),
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=True
    )

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp()
    )

    learner = db.relationship(
        "User",
        back_populates="learner_activities"
    )

    learning_activity = db.relationship(
        "LearningActivity",
        back_populates="learner_activities"
    )

    __table_args__ = (
        db.CheckConstraint(
            "score >= 0 AND score <= 100",
            name="check_activity_score_range"
        ),
    )

    def __repr__(self):
        return (
            f"<LearnerActivity "
            f"learner={self.learner_id}, "
            f"activity={self.activity_id}, "
            f"score={self.score}>"
        )
