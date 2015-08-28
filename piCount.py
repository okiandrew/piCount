# Raspberry Pi Counting System
# @author Andrew Rohne, OKI Regional Council, @okiAndrew, 8/25/2015

# LArge parts taken from https://github.com/berak/opencv_smallfry/blob/master/mjpg_serve.py

#FIXME: only takes an image when started, not continuously!

import cv2, sys, os, picamera, io, time, numpy
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

#cascPath = "C:\\Modelrun\\TruckModel\\RPi\\PiCount\\faceCascades\\haarcascade_frontalface_default.xml"



class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print self.path
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    runPath = os.path.join(os.path.dirname(sys.argv[0]))
                    cascPath = runPath + "\\cascade.xml"
                    faceCascade = cv2.CascadeClassifier(cascPath)
                    stream = io.BytesIO()
                    camera.capture(stream, format = 'jpeg')
                    data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
                    img = cv2.imdecode(data,1)
                    #for foo in camera.capture_continuous(stream,'jpeg'):
                    fr2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(fr2, scaleFactor = 1.3, minNeighbors = 5, minSize = (30,30), flags = cv2.CASCADE_SCALE_IMAGE)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(fr2, (x, y), (x+w, y+h), (0, 255, 0), 2)



                    r, buf = cv2.imencode(".jpg",fr2)
                    self.wfile.write("--jpgboundary\r\n")
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(len(buf)))
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                    self.wfile.write('\r\n')
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html') or self.path=="/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return

def main():
	#global capture
	#capture = cv2.VideoCapture(0)
	#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
	#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
    global camera
    camera = picamera.PiCamera()
    camera.resolution = (640,480)
    camera.hflip = True
    camera.vflip = True
    try:
        server = HTTPServer(('',9090),CamHandler)
        print "server started"
        server.serve_forever()
    except KeyboardInterrupt:
		#capture.release()
        #camera.release()
        server.socket.close()

if __name__ == '__main__':
	main()
