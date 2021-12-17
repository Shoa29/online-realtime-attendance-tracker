// connecting with socket
var socket = io('http://127.0.0.1:5000', {'force new connection': true});

// getting video displaying html object
const video = document.querySelector('#videoElement');
video.width = 500; 
video.height = 375; ;

// streaming webcam 
window.navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
            sendFrames()
        };
    })
    .catch( () => {
        alert('Give permissions to your browser');
    });

//send frames in every ~ 8 sec
function sendFrames() {
    const FPS = 24; 
    setInterval(() => {
        var studentid = document.getElementById('username');
        checkEvents();
        var img_data = captureFrame() // base64 of frame
        var type = "image/png"
        data = img_data.replace('data:' + type + ';base64,', ''); //remove junk
        socket.emit('frame', data, studentid.value); // sending base64 of captured frames
        
    }, 200000/FPS); //8 secs interval
    
    
}

//function to capture frames
function captureFrame() {
    var canvas = document.getElementById("canvasOutput");
    var context = canvas.getContext('2d');

    if (video.width && video.height) {
      canvas.width = video.width;
      canvas.height = video.height;
      context.drawImage(video, 0, 0, video.width, video.height);//canvas element displaying webcam video

      var data = canvas.toDataURL('image/png');// converting img to DataURI
      return data; // returning base64
    }
  }

//function to receive events from socket and output on frontend
function checkEvents(){
    const instructions = document.getElementById('instruction-text');
    var studentid = document.getElementById('username');
    socket.on('missing', function(){
        console.log("Student missing");
        instructions.innerHTML = 'Student Missing';
        instructions.style.color = 'red';
    });
    socket.on('wrong', function(){
        console.log("Wrong Student");
        instructions.innerHTML = 'Wrong Student';
        instructions.style.color = 'red';
    });
    socket.on('correct', function(){
        console.log("Correct Student");
        instructions.innerHTML = 'Welcome ' + studentid.value;
        instructions.style.color = 'white';
    });
}