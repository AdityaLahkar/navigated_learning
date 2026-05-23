from app.extensions import db


class TopicPrerequisite(db.Model):

    __tablename__ = "topic_prerequisites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    prerequisite_topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    next_topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id"),
        nullable=False
    )

    prerequisite_topic = db.relationship(
        "Topic",
        foreign_keys=[prerequisite_topic_id],
        back_populates="dependent_edges"
    )

    next_topic = db.relationship(
        "Topic",
        foreign_keys=[next_topic_id],
        back_populates="prerequisite_edges"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "prerequisite_topic_id",
            "next_topic_id",
            name="unique_prerequisite_edge"
        ),
    )

    def __repr__(self):
        return (
            f"<TopicPrerequisite "
            f"{self.prerequisite_topic_id} -> "
            f"{self.next_topic_id}>"
        )
