from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from task_allocation_api.API.db_utils import initialize_database, create_connection
# from flask_migrate import Migrate

from .Models.User import db, UserTemp, Task, bcrypt
from task_allocation_api.API.SignupPage import signup_api
from task_allocation_api.API.LoginPage import login_api
from task_allocation_api.API.TaskAllocation import task_allocation_api

app = Flask(__name__)
CORS(app)

initialize_database("localhost", "root", "root", "userstask")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/userstask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'This is My First Portfolio Project'
db.init_app(app)
bcrypt.init_app(app)

# migrate = Migrate(app, db)

# Check if the User table exists
with app.app_context():
    inspector = db.inspect(db.engine)
    if not inspector.has_table(UserTemp.__tablename__):
        db.create_all()
    if not inspector.has_table(Task.__tablename__):
        db.create_all()

# Register Blueprints
app.register_blueprint(signup_api)
app.register_blueprint(login_api)
app.register_blueprint(task_allocation_api)



@app.route("/")
def hello():
    return "Hello World"
def main():
    app.run(host="0.0.0.0", port=5000, debug=True)







# # Replace these values with your MySQL server credentials
# host = 'localhost'
# user = 'Omkar'
# password = 'Omkarj@1'
# database = 'users'