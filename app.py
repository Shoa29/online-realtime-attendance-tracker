from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from model import track_attendance

#creating instance of track_attendance module
tracker = track_attendance.FaceDatasetTrain()

app = Flask(__name__)
socketio = SocketIO(app)

#rendering frontend 
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print("Connected")

#on event frame -> checking student's identity
@socketio.on('frame')
def frame(data, studentname):
    print(studentname, " Frame Caught ")
    name = tracker.trackAttendance(data) # sending base64 of frame to model
    if name is None: #No student 
        print("---MISSING----")
        emit('missing', name)  
    elif name == "Unknown" or name !=studentname: #wrong person attending class
        print("---WRONG STUDENT----", name , " and ", studentname)
        emit('wrong', name)
    elif name==studentname: #correctly identified
        print("----CORRECT STUDENT----")
        emit("correct",name)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)