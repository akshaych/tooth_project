# the tooth project

import os

import flask
import flask_jwt_extended

import exceptions
import models
import views


app = flask.Flask(__name__)
jwt = flask_jwt_extended.JWTManager(app)

# app configs
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# views
app.add_url_rule("/token", view_func=views.token, methods=["POST"])
app.add_url_rule("/add_event", view_func=views.add_event, methods=["POST"])
app.add_url_rule("/get_events", view_func=views.get_events, methods=["GET"])

# exceptions
app.register_error_handler(exceptions.NoUserId, exceptions.handle_exception)
app.register_error_handler(exceptions.NoUserIdInToken, exceptions.handle_exception)
app.register_error_handler(exceptions.InvalidEventType, exceptions.handle_exception)
app.register_error_handler(exceptions.InvalidEventType, exceptions.handle_exception)
app.register_error_handler(exceptions.InvalidJson, exceptions.handle_exception)
app.register_error_handler(exceptions.InvalidDatetime, exceptions.handle_exception)
app.register_error_handler(exceptions.InvalidToothId, exceptions.handle_exception)


# db initialization
models.db.init_app(app)
models.db.create_all(app=app)


if __name__ == "__main__":
    app.run()
