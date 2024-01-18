from flask import Flask, request, render_template, Blueprint, json, jsonify, redirect, url_for
from task_allocation_api.Models.User import UserTemp,Task, db, bcrypt



login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_data = json.loads(request.data)

        print("user_data",user_data)
        # return jsonify({"message":'Login Successful'}), 200

        coll_data = UserTemp.query.filter_by(emailId=user_data["email"]).first()
        # print("coll_data",coll_data)
        if coll_data is None:
            return jsonify({"message":'There is no such account'}), 400

        check_pass = bcrypt.check_password_hash(coll_data.password, user_data["password"])
        
        if check_pass:
            return jsonify({"message":'Login Successful'}), 200
        else:
            return jsonify({"message":'Login Failed'}), 404

        

        # flash(error)

    # return render_template('auth/login.html')


@login_api.route("/all_users_get", methods=["GET"])
def User_All_get():
    if request.method == "GET":
        try:
            AllExtingUsers = UserTemp.query.all()
            if not AllExtingUsers:
                return jsonify({"Message":"There is no User"}), 404
            
            # Convert the query result to a list of dictionaries using __dict__
            All_Users = [task.__dict__ for task in AllExtingUsers]
            

            # Remove unnecessary keys (such as '_sa_instance_state')
            for user_dict in All_Users:
                user_dict.pop('_sa_instance_state', None)
                user_dict.pop('password', None)

            return jsonify(All_Users), 200
        
        except Exception as e:
            print("Error", str(e))
            return jsonify({"Error":str(e)}), 500

@login_api.route("/user_update", methods=["PUT"])
def User_Update_update():
    if request.method == "PUT":
        user_data = json.loads(request.data)
        # print("User data", user_data)

        try:
            existing_user = UserTemp.query.filter_by(emailId=user_data["emailId"]).first()
            if not existing_user:
                return jsonify({"Message":"There is no such user"}), 400
            
            if 'firstName' in user_data:
                existing_user.firstName = user_data["firstName"]

            if 'lastName' in user_data:
                existing_user.lastName = user_data["lastName"]

            if 'password' in user_data:
                hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')
                existing_user.password  = hashed_password

            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            print("Error updating",str(e))
            db.session.rollback()
            return jsonify({"Message":str(e)}), 400
        

@login_api.route("/user_delete/", methods=["DELETE"])
def User_Delete_delete():
    if request.method == "DELETE":
        try:
            emailId = request.args.get("emailId")

            if not emailId:
                return jsonify({"Message": "Please provide an email address"}), 400

            existing_user = UserTemp.query.filter_by(emailId=emailId).first()

            if not existing_user:
                return jsonify({"Message": "There is No Such User"}), 404
            

            tasks = Task.query.filter_by(emailId=emailId).all()
            for task in tasks:
                db.session.delete(task)

            db.session.delete(existing_user)
            db.session.commit()

            return jsonify({"Message": "User Deleted Successfully"}), 200

        except Exception as e:
            print("Exception:", str(e))
            return jsonify({"Error": str(e)}), 500
    
        
