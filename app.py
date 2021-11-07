from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from model import track_attendance

#creating instance of track_attendance module
tracker = track_attendance.FaceDatasetTrain()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print("Connected")

@socketio.on('frame')
def frame(data, studentid):
    print(studentid, " Frame Caught ")
    id = tracker.trackAttendance(data)
    if id is None:
        print("---MISSING----")
        emit('missing', id)  
    elif id == "Unknown" or id!=studentid:
        print("---WRONG STUDENT----", id, " and ", studentid)
        emit('wrong', id)
    elif id==studentid:
        print("--CORRECT STUDENT--")
        emit("correct",id)



if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', debug=True)