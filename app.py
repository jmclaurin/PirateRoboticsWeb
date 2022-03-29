#===================================================
#Robotic Arm 
#===================================================


from tracemalloc import stop
import cv2 
from realsense_camera import*

from flask import Flask, request, render_template, Response, request, redirect, url_for
#from core.water_bottle_routine import GripperCommandExample


import json, pickle, csv

#from core.company import Company
# from capstone2020.core.employee import Employee
# from capstone2020.core.resource import Resource
# import capstone2020.core.resource_provisioning as rp
# from capstone2020.core.parsing.syntax_tree import Syntax_Tree
# import capstone2020.core.usage_similarity as usage

import core.water_bottle_routine as wr
#from core.water_bottle_routine import GripperCommandExample 



app = Flask(__name__)

# Company Hierarchy Tree data#===================================================
#Robotic Arm 
#===================================================


from sre_constants import SUCCESS
import subprocess
from tkinter import NONE 
import cv2 

import time
import sys
import os
import threading

from core.camera import VideoCamera

sys.path.insert(0, '106-Gripper_command\01-gripper_command.py')

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.messages import Session_pb2, Base_pb2

from flask import Flask, request, render_template, Response, request, redirect, url_for
#from core.water_bottle_routine import GripperCommandExample



import json, pickle, csv

from matplotlib.pyplot import phase_spectrum
# import cv2 
# from realsense_camera import* 
#from realsense_camera import* 


#from core.company import Company
# from capstone2020.core.employee import Employee
# from capstone2020.core.resource import Resource
# import capstone2020.core.resource_provisioning as rp
# from capstone2020.core.parsing.syntax_tree import Syntax_Tree
# import capstone2020.core.usage_similarity as usage

import core.water_bottle_routine as wr
import core.ObjDetectionTest1 as ot
import core.PirateRobotics.api_python.examples.ObjDetectionTest1 as od 

#from core.water_bottle_routine import GripperCommandExample 
# from core.grocery_store_Web import *



app = Flask(__name__)

# Company Hierarchy Tree data
# company = pickle.load(open('./data/smalldata/small_company_object.pkl', 'rb'))
# employee_resources = json.load(open("./data/employee_resource_map.json", 'r'))

# Provisioning Metrics data
# employee_set = rp.load_company("./data/users.csv")
# resource_employee_map = rp.load_resource_map_from_csv("./data/user_resources.csv")

# Response protocols
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hierachyTree.html")
def hierachy_tree():
    return render_template("hierachyTree.html")


@app.route("/provisionMetrics.html")
def provision_metrics():
    return render_template("provisionMetrics.html")

@app.route("/test.html")
def test():
    return render_template("test.html")

@app.route("/camera_show", methods=["POST"])
def camera_show():
    subprocess.call("python grocery_store_Web.py")
    return render_template("test.html")

@app.route("/team.html")
def research():
    return render_template("team.html")

@app.route('/button_action')
def move_arm():
    print("this works")

@app.route("/api/distance", methods=["POST"])
def calculate_distance():
    body = json.loads(request.data)
    try:
        employee_one = company.search(int(body.get("employee_one_id")))
        employee_two = company.search(int(body.get("employee_two_id")))
        distance = company.distance(employee_one, employee_two)
    except Exception as e:
        print(e)
        return failure_response("One or more employees not found.", 404)
    return success_response(distance)

@app.route("/api/usage", methods=["POST"])
def calculate_usage():
    body = json.loads(request.data)
    try:
        employee_one = company.search(int(body.get("employee_one_id")))
        employee_two = company.search(int(body.get("employee_two_id")))
    except Exception as e:
        print(e)
        return failure_response("One or more employees not found in company.", 404)

    # Retrieve list of resources for employes
    employee_one_resources = employee_resources.get(str(employee_one.id))
    employee_two_resources = employee_resources.get(str(employee_two.id))

    # Check if no resources attached to employee
    if(employee_one_resources is None or employee_two_resources is None):
        return failure_response("No usage data for one or both of these employees.", 500)
    else:
        usage_similarity = usage.usage_similarity(employee_one_resources, employee_two_resources)
    return success_response(usage_similarity)

@app.route("/api/provisioning", methods=["POST"])
def calculate_provisioning():
    body = json.loads(request.data)
    resource_attr_1 = int(body.get("resource_attr_1"))
    resource_attr_2 = int(body.get("resource_attr_2"))
    rule = str(body.get("rule"))
    try:
        ast = Syntax_Tree(rule)
        resource = Resource(resource_attr_1, resource_attr_2)
        rp_metrics = rp.get_metrics(resource, ast, resource_employee_map, employee_set)
    except Exception as e:
        print(e)
        return failure_response("Invalid rule or resource passed.", 404)
    rp_metrics = (float("{:.2f}".format(rp_metrics[0])), float("{:.2f}".format(rp_metrics[1])))
    return success_response(rp_metrics)

@app.route("/move_to_home", methods=['POST'])
def move_to_home():
    #Moving forward code
    forward_message = "Moving Forward..."
    print("Hello world")
    #call main method from water_bottle_routine
    #wr.main()
    od.main()
    
   
    return render_template('test.html', forward_message=forward_message);

@app.route("/move_left", methods=['POST'])
def move_left():
    #Moving forward code
    forward_message = "Moving Forward..."
    print("Hello world")
    #call main method from water_bottle_routine
    #wr.main()
    wr.main()
   
    return render_template('test.html', forward_message=forward_message);

@app.route("/move_right", methods=['POST'])
def move_right():
    #Moving forward code
    forward_message = "Moving Forward..."
    print("Hello world")
    #call main method from water_bottle_routine
    #wr.main()
    ot.main()
   
    return render_template('test.html', forward_message=forward_message);

@app.route("/stop_move", methods=['POST'])
def stop_move():
    #stop moving code
    #subprocess.call("python manual.py")
    ot.main()
   
    return render_template('test.html', forward_message=forward_message);
#Move to home button 

#ObjDetectionTest1.example_move_to_home_position(base)

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

cap.set(cv2.CAP_PROP_FOURCC, 0x32595559)

cap.set(cv2.CAP_PROP_FPS, 25)

#####
def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=cap.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
# company = pickle.load(open('./data/smalldata/small_company_object.pkl', 'rb'))
# employee_resources = json.load(open("./data/employee_resource_map.json", 'r'))

# Provisioning Metrics data
# employee_set = rp.load_company("./data/users.csv")
# resource_employee_map = rp.load_resource_map_from_csv("./data/user_resources.csv")

# Response protocols
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hierachyTree.html")
def hierachy_tree():
    return render_template("hierachyTree.html")


@app.route("/provisionMetrics.html")
def provision_metrics():
    return render_template("provisionMetrics.html")

@app.route("/test.html")
def test():
    return render_template("test.html")

@app.route("/team.html")
def research():
    return render_template("team.html")

@app.route('/button_action')
def move_arm():
    print("this works")

@app.route("/api/distance", methods=["POST"])
def calculate_distance():
    body = json.loads(request.data)
    try:
        employee_one = company.search(int(body.get("employee_one_id")))
        employee_two = company.search(int(body.get("employee_two_id")))
        distance = company.distance(employee_one, employee_two)
    except Exception as e:
        print(e)
        return failure_response("One or more employees not found.", 404)
    return success_response(distance)

@app.route("/api/usage", methods=["POST"])
def calculate_usage():
    body = json.loads(request.data)
    try:
        employee_one = company.search(int(body.get("employee_one_id")))
        employee_two = company.search(int(body.get("employee_two_id")))
    except Exception as e:
        print(e)
        return failure_response("One or more employees not found in company.", 404)

    # Retrieve list of resources for employes
    employee_one_resources = employee_resources.get(str(employee_one.id))
    employee_two_resources = employee_resources.get(str(employee_two.id))

    # Check if no resources attached to employee
    if(employee_one_resources is None or employee_two_resources is None):
        return failure_response("No usage data for one or both of these employees.", 500)
    else:
        usage_similarity = usage.usage_similarity(employee_one_resources, employee_two_resources)
    return success_response(usage_similarity)

@app.route("/api/provisioning", methods=["POST"])
def calculate_provisioning():
    body = json.loads(request.data)
    resource_attr_1 = int(body.get("resource_attr_1"))
    resource_attr_2 = int(body.get("resource_attr_2"))
    rule = str(body.get("rule"))
    try:
        ast = Syntax_Tree(rule)
        resource = Resource(resource_attr_1, resource_attr_2)
        rp_metrics = rp.get_metrics(resource, ast, resource_employee_map, employee_set)
    except Exception as e:
        print(e)
        return failure_response("Invalid rule or resource passed.", 404)
    rp_metrics = (float("{:.2f}".format(rp_metrics[0])), float("{:.2f}".format(rp_metrics[1])))
    return success_response(rp_metrics)

@app.route("/test", methods=['POST'])
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    print("Hello world")
    #call main method from water_bottle_routine
    wr.main()
    return render_template('index.html', forward_message=forward_message);

@app.route("/your_flask_route")
def your_flask_route():
    import cv2 
 

#Load Realsese camera 
rs = RealsenseCamera() 


while True: 
    ret, bgr_frame, depth_frame = rs.get_frame_stream()

    point_x, point_y = 250, 100
    distance_mm = depth_frame[point_y, point_x]

    cv2.circle(bgr_frame, (point_x, point_y), 8, (0, 0, 255), -1)
    cv2.putText(bgr_frame, "{} mm".format(distance_mm), (point_x, point_y - 10), 0, 1, (0, 0, 255), 2)
    

    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Robotic Eyesight", bgr_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break 

if __name__ == "__main__":
    app.run()

@app.route('/')
def index():
  return render_template('index.html')
