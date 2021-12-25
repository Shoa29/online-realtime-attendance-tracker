import socketio
import base64
import timeit

student_name = "zynah"
sio = socketio.Client()
sio.connect("http://127.0.0.1:5000")

# testing static rendering
def test_static(app,client):
    del app
    landing = client.get("/")
    html = landing.data.decode()
    assert landing.status_code == 200
    assert "<title>Online Classe</title>" in html

# testing socket connection
@sio.event()
def connect():
    print("connection established")
    test_socket()


# testing timing + getting event on sending frame 
def test_socket():
    path = "assets/test_img.jpg"
    
    with open(path, "rb") as img:
        imgdata = base64.b64encode(img.read())
        sio.emit("frame", (imgdata, student_name) )
        start = timeit.default_timer() 
        print("emitted frame")

        @sio.on("wrong")
        def wrongStudent(data):
            end = timeit.default_timer() 
            finish = end - start
            print(f' Time Taken {finish}')
            print(" Wrong Student Received ", data)
        
        @sio.on("correct")
        def correctStudent(data):
            end = timeit.default_timer() 
            finish = end - start
            print(f' Time Taken {finish}')
            print(" Correct Student Received ", data)
        
        @sio.on("missing")
        def missingStudent(data):
            end = timeit.default_timer() 
            finish = end - start
            print(f' Time Taken {finish}')
            print(" Missing Student Received ", data)

    

    



