var socket = io('http://127.0.0.1:5000', {'force new connection': true});
console.log("entered script "+ socket);
const video = document.querySelector('#videoElement');
video.width = 500; 
video.height = 375; ;
//Core
window.navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
        };
    })
    .catch( () => {
        alert('You have give browser the permission to run Webcam and mic ;( ');
    });
    //send frames
function onOpenCvReady() {
    console.log('OpenCV.js is ready');
    let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    let cap = new cv.VideoCapture(video);
    const FPS = 22;
    setInterval(() => {
        var studentid = document.getElementById('username');
        checkEvents();
        cap.read(src);
        var imgdata = takeFrame()
        var type = "image/png"
        //var data = document.getElementById("canvasOutput").toDataURL(type);
        data = imgdata.replace('data:' + type + ';base64,', ''); //split off junk 
        console.log("Frame caught "+ data);
        //send room id as well
        socket.emit('frame', data, studentid.value);
        
    }, 200000/FPS);
    
    
}
function takeFrame() {
    var canvas = document.getElementById("canvasOutput");
    var context = canvas.getContext('2d');
    if (video.width && video.height) {
      canvas.width = video.width;
      canvas.height = video.height;
      context.drawImage(video, 0, 0, video.width, video.height);

      var data = canvas.toDataURL('image/png');
      console.log(data);
      //photo.setAttribute('src', data);
      return data;
    }
  }
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