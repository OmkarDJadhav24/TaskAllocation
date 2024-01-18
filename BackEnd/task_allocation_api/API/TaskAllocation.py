from flask import Flask, request, render_template, Blueprint, json, jsonify, redirect, url_for
from task_allocation_api.Models.User import UserTemp,Task,db, bcrypt


task_allocation_api = Blueprint('task_allocation_api', __name__)

@task_allocation_api.route("/task_allocation", methods=["POST"])
def task_allocation_post():
    if request.method == "POST":
        task_data = json.loads(request.data)
        if  not task_data:
            return jsonify({"message":'Please provide task details.'}), 400

        try:
            existing_task = Task.query.filter_by(taskName=task_data["taskName"]).first()
            
            if existing_task:
                return jsonify({"message":'Task already exists. Please choose a different one.'}), 400

            last_task = Task.query.order_by(Task.id.desc()).first()
            last_task_id = last_task.id if last_task else 0
            last_task_id = last_task_id + 1
            
            # Create Instance of UserTemp Model
            insert_task_query = Task(id=last_task_id,taskName=task_data["taskName"],taskDescription=task_data["taskDescription"],emailId=task_data["emailId"])
            
            #Add instance to Session
            db.session.add(insert_task_query)
            #Commit the session to save changes to database
            
            db.session.commit()
            print("existing_task",existing_task)
            
            return jsonify({"Message":"Task Allocation Successful"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"Message":str(e)}), 500



@task_allocation_api.route("/singletask/", methods=["GET"])
def task_allocation_get():
    if request.method == "GET":
        emailId = request.args.get("emailId")
        if not emailId:
            return jsonify({"Message":"Please Provide emailId"})
        
        try:
            user_check = UserTemp.query.filter_by(emailId=emailId).first()
            if not user_check:
                return jsonify({"Message":"User does not exist"}),404
            
            user_details = Task.query.filter_by(emailId=emailId).all()
            if not user_details:
                return jsonify({"Message":"There is no task for that user"}),404

            # Convert the query result to a list of dictionaries using __dict__
            user_data = [user.__dict__ for user in user_details]            

            # Remove unnecessary keys (such as '_sa_instance_state')
            for user_dict in user_data:
                user_dict.pop('_sa_instance_state', None)

            return jsonify(user_data), 200
        except Exception as e:
            return jsonify({"Message":str(e)}), 400
        

@task_allocation_api.route("/alltasks/", methods=["GET"])
def get_all_tasks():
    try:
        task_info = Task.query.all()
        if not task_info:
                return jsonify({"Message":"There is no task"}),404

        # Convert the query result to a list of dictionaries using __dict__
        user_data = [task.__dict__ for task in task_info]
        
        # Remove unnecessary keys (such as '_sa_instance_state')
        for user_dict in user_data:
            user_dict.pop('_sa_instance_state', None)

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"Message":str(e)}), 400
    

@task_allocation_api.route("/delete_task/", methods=["DELETE"])
def delete_task():
    if request.method == "DELETE":
        taskName = request.args.get("taskName")

        try:
            existing_task = Task.query.filter_by(taskName=taskName).first()

            db.session.delete(existing_task)
            db.session.commit()
            return jsonify({"Message":"Task Deleted Successfully"})
        
        except Exception as e:
            return jsonify({"Error":str(e)}), 500