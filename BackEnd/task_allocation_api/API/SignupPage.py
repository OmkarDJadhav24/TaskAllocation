from flask import Flask, request, render_template, Blueprint, json, jsonify, redirect, url_for
# from werkzeug.security import check_password_hash, generate_password_hash
from task_allocation_api.Models.User import UserTemp,db, bcrypt



signup_api = Blueprint('signup_api', __name__)

@signup_api.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        user_data = json.loads(request.data)
        # print(user_data)
        try:
            # print("user_data", user_data)
            existing_user = UserTemp.query.filter_by(emailId=user_data["emailId"]).first()

            if existing_user:
                return jsonify({"message":'Username already exists. Please choose a different one.'}), 407
            

            # Logic to save data in database if already not exists.
            
            # Calculate the new user's ID
            last_user = UserTemp.query.order_by(UserTemp.id.desc()).first()
            last_user_id = last_user.id if last_user else 0
            new_user_id = last_user_id + 1
            
            # Generate Hash Value of Password
            hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')

            # Create Instance of UserTemp Model
            insert_user_query = UserTemp(id=new_user_id, firstName=user_data["firstName"], lastName=user_data["lastName"], emailId=user_data["emailId"], password=hashed_password)
            #Add instance to Session
            db.session.add(insert_user_query)
            #Commit the session to save changes to database
            db.session.commit()
            
            return jsonify({"Message":"Registration Successful"}), 200
        except Exception as e:
            print("Error:", str(e))  # Log the error for debugging
            return jsonify({"Message": str(e)}), 400
    



@signup_api.route("/signup/", methods=["GET"])
def user_get():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"Message":"Please Provide User Id"})
        
        try:
            user_id = int(user_id)

            user_check = UserTemp.query.filter_by(id=user_id).first()
            if not user_check:
                return jsonify({"Message":"User does not exist"}),404



            # Convert the query result to a list of dictionaries using __dict__
            user_data = [user.__dict__ for user in user_check]
            

            # Remove unnecessary keys (such as '_sa_instance_state')
            for user_dict in user_data:
                user_dict.pop('_sa_instance_state', None)


            return jsonify(user_data), 200
        except Exception as e:
            return jsonify({"Message":str(e)}), 400
    



@signup_api.route("/allusers/", methods=["GET"])
def get_all():

    try:
        user_check = UserTemp.query.all()
        if not user_check:
            return jsonify({"Message":"There is no User. Please Add Some Users"}),404



        # Convert the query result to a list of dictionaries using __dict__
        user_data = [user.__dict__ for user in user_check]
        

        # Remove unnecessary keys (such as '_sa_instance_state')
        for user_dict in user_data:
            user_dict.pop('_sa_instance_state', None)


        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"Message":str(e)}), 400