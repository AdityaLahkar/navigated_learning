from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, migrate, jwt


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    # to avoid circular imports
    from app.models import (
        User,
        Topic,
        TopicPrerequisite,
        LearnerTopicProgress,
        LearningActivity,
        LearnerActivity
    )

    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)

    from app.routes.learner_routes import learner_bp
    from app.routes.teacher_routes import teacher_bp

    app.register_blueprint(learner_bp)
    app.register_blueprint(teacher_bp)

    from app.routes.topic_routes import topic_bp

    app.register_blueprint(topic_bp)


    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "error": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):

        return jsonify({
            "error": "Internal server error"
        }), 500

    return app