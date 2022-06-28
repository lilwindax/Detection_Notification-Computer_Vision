# Import Libraries 
import cv2  # Open CV Libary
import mediapipe as mp # Mediapipe lib by google for cloud based ML applications
import time # Time lib - used to display the frame rates
from twilio.rest import Client # Rest API from Twilio - Communications platform

cap = cv2.VideoCapture(0)   # Run the webcam
pTime = 0   # Initialize the prev time to 0
i = 1 # Initialize the i counter for the face dectection to 1

mpFaceDetection = mp.solutions.face_detection  # Get the Face Detection from the Media Pipe
mpDraw = mp.solutions.drawing_utils     # For drawing rectangle around the detected face and the facial points
faceDetection = mpFaceDetection.FaceDetection(0.75) # Initialize the function used

account_sid = 'account id'  # Twilio account id
auth_token = 'authentication token'   # Twilio Auth Token
client = Client(account_sid, auth_token)   # Calling the Function through API

while True:
    success, img = cap.read()   # Frame

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # Convert the webcam live footage to RGB
    results = faceDetection.process(imgRGB)     # Process imgRGB using the Media Pipe

    if results.detections:  # Check the detections
        for id, detection in enumerate(results.detections): # Loop through the results and display them
            mpDraw.draw_detection(img, detection)   # Draw the bounding box to the detected faces and facial features
            bboxC = detection.location_data.relative_bounding_box # Restore class access into new variable
            ih, iw, ic, = img.shape     # Setting the positions of the img
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)    # Set the x, y, c for the bounding box
            # cv2.rectangle(img, bbox, (255, 0, 255), 2) # Display the rectangle without the facial features
            cv2.putText(img, f'Score: {int(detection.score[0]*100)}%', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255),
                        2)  # Display the score of detection

            # Condition to check when a face is detected
            if i == 1:  # If more then one person is to be detected then the statement can be changed to || i == 2......
                #  i=i+1
                if (detection.score[0] * 100 > 90):
                     message = client.messages.create(from_='whatsapp:+14155238886', body='Detection Sucessful',to='whatsapp:+endestinationphonenumber')

                    i = i + 1
                    print('Successful')

            # print(id, detection) # The detections and their keypoints
            # print(detection.score)  # How much the model thinks a detection is a Face
            # print(detection.location_data.relative_bounding_box)  # The location data for bounding box

    cTime = time.time()      # Get the ime
    fps = 1/(cTime-pTime)   # Calculate the fps
    pTime = cTime   # Reset pTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)   # Displaying the fps to the window
    cv2.imshow('Image', img)  # Window displaying webcam

    cv2.waitKey(1)  # Can alter the frame rate

    if cv2.waitKey(1) & 0xFF == ord('q'):   # Quit the window when q is pressed
        break



