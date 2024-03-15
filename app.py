from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import cv2
from ultralytics import YOLO
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nurye@68793'
app.config['MYSQL_DB'] = 'traffic_light'
mysql = MySQL(app)
model = YOLO(r"C:\Users\hp\Desktop\software_HILCOE\traffic_light_control_system\static\notebooks\runs\detect\train\runs\detect\train8\weights\best.pt")
@app.route('/predict_cars', methods=['GET'])
def predict_cars():
    video_path = r"C:\Users\hp\Desktop\software_HILCOE\traffic_light_control_system\model\junction\video1.mp4"
    cap = cv2.VideoCapture(video_path)
    car_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=0.7)
        car_count += len(results)
        car_counting = int(round(car_count * (1 - 0.85)))
    cap.release()
    return jsonify({'car_count': car_counting})
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM squires")
    squires_data = cur.fetchall()
    cur.close()
    return render_template('home.html', squires=squires_data)
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    name = request.form['name']
    phone = request.form['phone']
    description = request.form['description']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO comment (name, phone, description) VALUES (%s, %s, %s)", (name, phone, description))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Comment submitted successfully!'})
@app.route('/workflow')
def workflow():
    return render_template('workflow.html')
@app.route('/display')
def display():
    
    squire_name = request.args.get('squireName')
    map_location = request.args.get('mapLocation')
    car_count = request.args.get('carCount')
    cur = mysql.connection.cursor()
    cur.execute("SELECT Junction1, Junction2, Junction3, Junction4 FROM squires WHERE Name = %s", (squire_name,))
    junction_row = cur.fetchone()
    cur.close()
    junctions = {}
    for i, junction_name in enumerate(junction_row, start=1):
        if junction_name:
            junctions[f'Junction {i}'] = junction_name

    
    return render_template('display.html', squireName=squire_name, junction_data=junctions, map_location=map_location, car_count=car_count)


if __name__ == '__main__':
    app.run(debug=True)
