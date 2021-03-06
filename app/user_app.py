# from app_init.app_factory import create_app
from flask import Blueprint
from app.models import ToDo, Users
from extensions.extension import db
from app.serializer import TodoSchema, ToDoUpdateSchema, UserSchema, UserUpdateSchema, UserUpdateFormSchema
from app.utils import verify_password
from extensions.extension import login_manager
from extensions.extension import csrf
from app.forms import SignUpForm, LoginForm, PassChangeForm
from app.utils import get_hash_password

from flask import request, jsonify, make_response, render_template, url_for, redirect, flash
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt_claims
from flask_login import login_required, login_user, logout_user, current_user
import os
from datetime import timedelta
import warnings


# telegram bot

warnings.simplefilter("ignore")
# settings_name = os.getenv("APP_SETTINGS")
# app = create_app(settings_name)
user_app = Blueprint("user_app", __name__)

# Users part:
@user_app.route("/api/users", methods=["POST"])
@csrf.exempt
def create_user():
    data = request.get_json()
    try:
        user = UserSchema().load(data)
        user.save_db()
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as err:
        return jsonify({"result": str(err)}), 400
    return UserSchema(exclude=("password",)).jsonify(user)


@user_app.route("/api/users", methods=["GET"])
@csrf.exempt
def get_users_results():
    results = Users.query.all()
    return UserSchema(exclude=("password",)).jsonify(results, many=True)


@user_app.route("/api/users/<id>", methods=["GET"])
@csrf.exempt
def get_user_id(id):
    data = Users.query.filter_by(id=id).first()
    if data:
        return UserSchema(exclude=("password",)).jsonify(data)
    return jsonify({"result": f"Id {id} wasn't found"}), 404


@user_app.route("/api/users/<id>", methods=["PUT"])
@csrf.exempt
def update_user_id(id):
    result = Users.query.filter_by(id=id).first()
    if result:
        data = request.json
        data = UserUpdateSchema().load(data)
        result = result.update_db(**data)
        return UserSchema(exclude=("password",)).jsonify(result)
    return jsonify({"result": f"Id {id} wasn't found"}), 404


@user_app.route("/api/users/<id>", methods=["DELETE"])
@csrf.exempt
def delete_user_id(id):
    data = Users.query.filter_by(id=id).first()
    # user_claims = get_jwt_claims()
    # if user_claims.get("is_admin"):

    if data:
        data.delete_from_db()
        return jsonify({"result": f"Id {id} was deleted"})

    return jsonify({"result": f" Id {id} wasn't found"}), 404


@user_app.route("/api/users/login", methods=["POST"])
@csrf.exempt
def user_login():
    data = request.json
    user = Users.query.filter_by(email=data.get("email").lower()).first()
    print(user)
    if user:
        if verify_password(data.get("password"), user.password):
            # user_claims={"is_admin": True} tokene elave options vermek ucundu ; fresh=True tokenin tezeliyin teyin etmek ucun
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(
                identity=user.id, expires_delta=timedelta(minutes=1))
            return jsonify(username=user.name, access_token=access_token, refresh_token=refresh_token)
    return jsonify({"message": "email or password incorrect"}), 404


@user_app.route("/api/users/info", methods=["GET", "POST"])
@csrf.exempt
@jwt_required
def get_user_info():
    id = get_jwt_identity()
    user = Users.query.get(id)
    if user:
        return UserSchema(exclude=("password",)).jsonify(user)
    return jsonify({"message": f"User wasn't found"}), 404


@user_app.route("/api/users/refresh", methods=["POST", "GET"])
@csrf.exempt
@jwt_refresh_token_required
def refresh_user_token():
    id = get_jwt_identity()
    user = Users.query.get(id)
    if user:
        access_token = create_access_token(identity=id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Token wasn't verified"}), 401

# For HTML connection
@user_app.route("/users/register", methods=["GET", "POST"])
def register():
    form = SignUpForm()

    if form.validate_on_submit():
        data = dict(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data
        )
        # user = UserSchema().load(data)
        user = Users(**data)
        user.password = get_hash_password(user.password)
        user.save_db()
        login_user(user)
        return redirect(url_for("user_app.dashboard"))

    return render_template("register.html", form=form)


@user_app.errorhandler(404)
def not_found_page(e):
    return render_template("404page.html")


@user_app.errorhandler(500)
def error_page(e):
    return render_template("500_error.html")


@user_app.route("/users/", methods=["GET"])
@user_app.route("/users/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html", form=current_user)


@user_app.route("/users/login", methods=["POST", "GET"])
def login_user_html():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user:
            if verify_password(password, user.password):
                login_user(user)
                return redirect(url_for("user_app.dashboard"))
        flash("User not found")
    return render_template("login.html", form=form)


@user_app.route("/users/editpass", methods=["POST", "GET"])
def edit_pass():
    form = PassChangeForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        data = dict(
            email=form.email.data,
            password=form.password.data
        )
        if user:
            data = UserUpdateFormSchema().load(data)
            user = user.update_db(**data)
            return redirect(url_for("user_app.login_user_html"))
        flash("User not found")
    return render_template("editpass.html", form=form)


@user_app.route("/users/editinfo", methods=["POST", "GET"])
@login_required
def edit_profile():
    form = SignUpForm()
    if form.validate_on_submit():
        data = dict(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=get_hash_password(form.password.data)
        )
        user = current_user
        user.update_db(**data)
        return redirect(url_for("user_app.dashboard"))
    return render_template("update.html", form=form, user=current_user)


@user_app.route("/users/todo", methods=["POST", "GET"])
@login_required
def todo_profile():
    pass

# Flask Login stuff
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('user_app.login_user_html'))


@user_app.route("/users/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("user_app.login_user_html"))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Users.query.get(user_id)
    return None
